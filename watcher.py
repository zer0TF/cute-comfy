import json
import os
import re
import threading
import time
import yaml
import requests

from PIL import Image
from PIL.PngImagePlugin import PngInfo
from watchdog import events, observers
from .utils import cuteprint

# PNG files are the only files that can carry metadata inside AND the only ones that we can parse/support (for now).
ALLOWED_EXTS = ['png']

# Per Comfy source, these are "active" or event-based (i.e. not bypassed/muted/disabled).
ENABLED_NODE_MODES = [0, 1, 3]

NODE_TYPES_CLIP_TEXT = ['CLIPTextEncode', 'PrimitiveNode']
NODE_TYPES_CIV_CKPT = ['CivitAI_Checkpoint_Loader']
NODE_TYPES_CIV_LORA = ['CivitAI_Lora_Loader']
NODE_TYPES_SAMPLER = ['KSampler', 'KSampler (Efficient)']

NODE_TITLE_PREFERRED_SAMPLER = 'Sampler'
NODE_TITLE_PREFERRED_POSITIVE = 'Positive'
NODE_TITLE_PREFERRED_NEGATIVE = 'Negative'

SAMPLER_NAME_MAP = {
    'euler': 'Euler',
    'euler_ancestral': 'Euler a',
    'heun': 'Heun',
    'dpm_2': 'DPM2',
    'dpm_2_ancestral': 'DPM2 a',
    'lms': 'LMS',
    'dpm_fast': 'DPM Fast',
    'dpm_adaptive': 'DPM Adaptive',
    'dpmpp_2s_ancestral': 'DPM++ 2S a',
    'dpmpp_sde': 'DPM++ SDE',
    'dpmpp_sde_gpu': 'DPM++ SDE',
    'dpmpp_2m': 'DPM++ 2M',
    'dpmpp_2m_sde': 'DPM++ 2M SDE',
    'dpmpp_2m_sde_gpu': 'DPM++ 2M SDE',
    'dpmpp_3m_sde': 'DPM++ 3M SDE',
    'dpmpp_3m_sde_gpu': 'DPM++ 3M SDE',
    'ddpm': 'DDPM',
    'ddim': 'DDIM',
    'uni_pc': 'UniPC',
    'uni_pc_bh2': 'UniPC BH2'
}

SCHEDULER_NAME_MAP = {
    'normal': '',
    'karras': 'Karras',
    'exponential': 'Exponential',
    'sgm_uniform': 'SGM Uniform',
    'simple': 'Simple',
    'ddim_uniform': 'Uniform'
}

Verbose = False

def init_watcher():
    global Verbose

    cur_dir = os.path.dirname(os.path.realpath(__file__))
    config_path = os.path.join(cur_dir, 'config.yaml')

    # If the file does not exist, this is a first-time run and we need to write the default one.
    if not os.path.exists(config_path):
        write_default_config(config_path)
        cuteprint('❣️➡️ First-time file watcher setup - please edit the config.yaml file located in the folder: "ComfyUI/custom_nodes/cute-comfy"')
        cuteprint('Disabling the file watcher just this one time, please restart ComfyUI after you\'ve modified the config file!')
        return

    try:
        with open(config_path, 'r') as f:
            config_dict = yaml.load(f, Loader=yaml.FullLoader)
    except:
        cuteprint('❌ Failed to load config.yaml. Please check the file for syntax errors.')
        return
    
    if not validate_config(config_dict):
        return
    
    Verbose = config_dict['watcher']['verbose']

    for folder in config_dict['watcher']['folders']:
        folder = folder.rstrip('\\').rstrip('/')
        watch_directory(folder, config_dict)

def watch_directory(dir, config_dict):
    global Verbose
    cuteprint(f'👁️ I\'m keeping an eye on: {dir}')

    watcher = observers.Observer()
    handler = events.FileSystemEventHandler()

    def on_created(event):
        # Ignore this file if the file name ends with our own write suffix, so that we don't get stuck in a loop.
        if event.src_path.endswith(config_dict['watcher']['write_suffix'] + '.' + event.src_path.split('.')[-1]):
            return

        cuteprint(f'👀 I see a new file, waiting for it to finish writing: {event.src_path}') if Verbose else None

        # Wait for the file to be fully written.
        # The watcher triggers on the file creation event, not when it's "done" writing.
        size = os.path.getsize(event.src_path)
        while True:
            time.sleep(1)
            if size == os.path.getsize(event.src_path):
                break
            else:
                size = os.path.getsize(event.src_path)

        update_metadata(event.src_path, config_dict)

    handler.on_created = on_created
    watcher.schedule(handler, dir, recursive=True)
    watcher.start()


def update_metadata(file, config_dict):
    global Verbose

    if not file.endswith(tuple(config_dict['watcher']['extensions'])):
        return

    cuteprint(f'👀 Attempting metadata update for: {file}') if Verbose else None

    with Image.open(file) as img:
        metadata = img.info

        if not metadata or 'workflow' not in metadata:
            cuteprint(f'👀 This file has no metadata, can\'t do anything: {file}') if Verbose else None
            return

        # Parse the metadata from a JSON string.
        workflow = json.loads(metadata['workflow'])

        # Get the node list
        nodelist = workflow['nodes']

        # Get all of the "common" metadata
        prompt_positive = get_metadata_clip_text(nodelist, NODE_TITLE_PREFERRED_POSITIVE)
        prompt_negative = get_metadata_clip_text(nodelist, NODE_TITLE_PREFERRED_NEGATIVE)
        ckpt_sha256 = get_metadata_ckpt_sha256(nodelist)
        lora_ckpt_sha256_list = get_lora_ckpt_sha256(nodelist)
        sampler, seed, steps, cfg = get_metadata_sampler(nodelist)

        # Build the Hashes JSON object
        hashes = {}
        if ckpt_sha256:
            hashes['model'] = ckpt_sha256
        if lora_ckpt_sha256_list:
            for i, lora_ckpt_sha256 in enumerate(lora_ckpt_sha256_list):
                hashes[f'lora:comfy2auto_converted_{i}'] = lora_ckpt_sha256
        hashes_json = json.dumps(hashes)

        # Write the new metadata to the file.
        new_metadata = f'''{prompt_positive if prompt_positive else ''}
Negative prompt: {prompt_negative if prompt_negative else ''}
{f'Steps: {steps}, ' if steps else ''}{f'Sampler: {sampler}, ' if sampler else ''}{f'CFG scale: {cfg}, ' if cfg else ''}{f'Seed: {seed}, ' if seed else ''}{f'AutoConverter: Cute Comfy, '}{f'Hashes: {hashes_json}'}
'''
        metadata = PngInfo()
        metadata.add_text("parameters", new_metadata)

        if config_dict['watcher']['overwrite']:
            img.save(file, pnginfo=metadata)
            cuteprint(f'👀 💜 Updated Civitai-compatible metadata inside file: {file}')
        else:
            new_file = file.replace(f'.{file.split(".")[-1]}', f'{config_dict["watcher"]["write_suffix"]}.{file.split(".")[-1]}')
            img.save(new_file, pnginfo=metadata)
            cuteprint(f'👀 💜 Updated Civitai-compatible metadata inside new file: {new_file}')



def get_metadata_clip_text(nodelist, title, skip_reformat = False) -> str | None:
    global Verbose
    for node in nodelist:
        if ('type' in node and node['type'] in NODE_TYPES_CLIP_TEXT) and 'title' in node and title in node['title'] and 'mode' in node and node['mode'] in ENABLED_NODE_MODES:
            if skip_reformat:
                return node['widgets_values'][0]
            else:
                return node['widgets_values'][0].replace('\r', '').replace('\n', ' ').strip()

    cuteprint(f'👀 Warning: No "{title}" metadata found.') if Verbose else None
    return None

def get_metadata_sampler(nodelist):
    global Verbose
    sampler = get_best_fit_sampler_node(nodelist)
    if sampler is None:
        cuteprint(f'👀 Warning: No "Sampler" metadata found.') if Verbose else None
        return None
    
    # If widgets_values has 7 items, it's a KSampler node.
    if len(sampler['widgets_values']) == 7:
        name, scheduler = sampler['widgets_values'][4], sampler['widgets_values'][5]
        seed = sampler['widgets_values'][0]
        steps = int(sampler['widgets_values'][2])
        cfg = int(sampler['widgets_values'][3])
    
    # If widgets_values has 10 items, it's a KSampler (Efficient) node.
    elif len(sampler['widgets_values']) == 10:
        name, scheduler = sampler['widgets_values'][5], sampler['widgets_values'][6]
        seed = sampler['widgets_values'][1]
        steps = int(sampler['widgets_values'][3])
        cfg = int(sampler['widgets_values'][4])

    # If widgets_values has any other number of items, it's not a KSampler node.
    else:
        cuteprint(f'👀 Warning: No compatible KSampler node found.') if Verbose else None
        return None
    
    # If the name or scheduler is empty, exit.
    if not name or not scheduler:
        cuteprint(f'👀 Warning: Selected KSampler node is missing its name or scheduler parameter.') if Verbose else None
        return None
    
    # Map the name and scheduler to the correct values.
    return map_sampler_name(name, scheduler), seed, steps, cfg
    

def map_sampler_name(name, scheduler) -> str:
    a1name = SAMPLER_NAME_MAP[name] if name in SAMPLER_NAME_MAP else name.capitalize()    
    a1sampler = SCHEDULER_NAME_MAP[scheduler] if scheduler in SCHEDULER_NAME_MAP else scheduler.capitalize()
    return f'{a1name} {a1sampler}'.strip()


def get_best_fit_sampler_node(nodelist) -> dict | None:
    global Verbose

    for node in nodelist:
        if 'title' in node and node['title'] == NODE_TITLE_PREFERRED_SAMPLER and 'mode' in node and node['mode'] in ENABLED_NODE_MODES:
            return node
    
    for node in nodelist:
        if 'type' in node and node['type'] in NODE_TYPES_SAMPLER and 'mode' in node and node['mode'] in ENABLED_NODE_MODES:
            return node
    
    cuteprint(f'👀 Warning: No "Sampler" node found.') if Verbose else None
    return None


def get_metadata_ckpt_sha256(nodelist) -> str | None:
    """
    Retrieves the SHA256 hash of the primary file of the Civitai Checkpoint AIR found in the given node list.
    """
    global Verbose
    civitai_air = get_civitai_air_from_node(nodelist, "CivitAI_Checkpoint_Loader", warn = True)
    if civitai_air is None:
        return None
    
    model_version = civitai_air.split('@')[-1]

    # Or: https://civitai.com/models/aaaaaa/?modelVersionId=bbbbbb
    resp = requests.get(f'https://civitai.com/api/v1/model-versions/{model_version}')
    if resp.status_code != 200:
        cuteprint(f'👀 Warning: Failed to fetch model info from Civitai API. Status code: {resp.status_code}') if Verbose else None
        return None
    
    resp_json = resp.json()
    primary_file = next((file for file in resp_json['files'] if file['primary']), None)

    if primary_file is None:
        cuteprint(f'👀 Warning: No primary file found in the model info response. Check API: https://civitai.com/api/v1/model-versions/{model_version}') if Verbose else None
        return None
    
    cuteprint(f'👀 Fetched AutoV2 ID from Civitai.com: {primary_file["name"]} = {primary_file["hashes"]["AutoV2"].lower()}') if Verbose else None

    return primary_file['hashes']['AutoV2'].lower()


def get_lora_ckpt_sha256(nodelist):
    """
    Retrieves a list of SHA256 hashes of the primary files of all Civitai LoRA AIRs found in the given node list.
    """
    global Verbose
    civitai_air_list = get_civitai_air_from_node(nodelist, "CivitAI_Lora_Loader", multiple = True)
    if civitai_air_list is None or len(civitai_air_list) == 0:
        return None
    
    lora_hashes = []

    for civitai_air in civitai_air_list:

        model_version = civitai_air.split('@')[-1]

        resp = requests.get(f'https://civitai.com/api/v1/model-versions/{model_version}')
        if resp.status_code != 200:
            cuteprint(f'👀 Warning: Failed to fetch model info from Civitai API. Status code: {resp.status_code}') if Verbose else None
            return None
        
        resp_json = resp.json()
        primary_file = next((file for file in resp_json['files'] if file['primary']), None)

        if primary_file is None:
            cuteprint(f'👀 Warning: No primary file found in the model info response. Check API: https://civitai.com/api/v1/model-versions/{model_version}') if Verbose else None
            return None
                
        lora_hashes.append(primary_file['hashes']['AutoV2'].lower())
    
    return lora_hashes if len(lora_hashes) > 0 else None


def get_civitai_air_from_node(nodelist, node_type, multiple = False, warn = False):
    """
    Attempts to extract a Civitai AIR from the given node list. Optionally, if multiple is set to True, returns a list of all Civitai AIRs found.
    """
    global Verbose
    air_ids = []
    for node in nodelist:
        if 'widgets_values' in node and 'type' in node and node['type'] == node_type and 'mode' in node and node['mode'] in ENABLED_NODE_MODES:
            
            air_id = None
            if 'inputs' in node:
                link = next((input['link'] for input in node['inputs'] if input['name'] == 'ckpt_air' or input['name'] == 'lora_air'), None)
                if link is not None:
                    air_id = walk_nodes_recursive(nodelist, link)

            if air_id is None:
                air_id = node['widgets_values'][0]
                if not re.match(r'\d+@\d+', air_id):
                    cuteprint(f'👀 Warning: The "{node_type}" node has an invalid AIR: {air_id}') if Verbose else None
                    return None
            
            if not multiple:
                return air_id
            else:
                air_ids.append(air_id)
    
    if multiple and len(air_ids) > 0:
        return air_ids
    
    cuteprint(f'👀 Warning: No Civitai model metadata found (did you use the "{node_type}" node type somewhere?).') if Verbose and warn else None
    return None

def walk_nodes_recursive(nodes, node_id):
    """
    Walks the node tree backwards recursively, looking for the first non-reroute node.
    """
    
    # Get the target node by ID.
    # We do this by looking inside each node, looking inside the "outputs" array, and if any objects in the "outputs" array have a "link" array containing the node_id, then that is our new target.
    target_node = None
    for node in nodes:
        if 'outputs' in node and len(node['outputs']) > 0:
            for output in node['outputs']:
                if 'links' in output and output['links'] is not None and len(output['links']) > 0 and node_id in output['links']:
                    target_node = node
                    break
        
    # If the target node is None, exit.
    if target_node is None:
        cuteprint(f'👀 Warning: Reached dead-end while traversing reroute notes for node ID: {node_id}') if Verbose else None
        return None
    
    # If this node is a reroute, recursively walk back to the next node.
    if 'type' in target_node and target_node['type'] == 'Reroute':
        return walk_nodes_recursive(nodes, target_node['inputs'][0]['link'])
    else:
        return target_node['widgets_values'][0] if 'widgets_values' in target_node and len(target_node['widgets_values']) > 0 else None


def write_default_config(path):
    default_config_dict = {
        'watcher': {
            'enabled': True,
            'overwrite': False,
            'write_suffix': '__a1',
            'verbose': False,
            'folders': [
                'Z:\Path\To\Your\Comfy\Output\Folder'
            ],
            'extensions': [
                'png'
            ]
        }
    }

    with open(path, 'w') as f:
        yaml.dump(default_config_dict, f)

def validate_config(config_dict):
    # If the watcher is not enabled, exit.
    if not config_dict['watcher']['enabled']:
        cuteprint('⚠️ File watcher is not enabled in config.yaml. Output files will not be automatically updated with Automatic1111-compatible metadata.')
        return False

    # If the watcher is enabled, but no folders are being watched, exit.
    if not config_dict['watcher']['folders']:
        cuteprint('⚠️ No folders are being watched in config.yaml. Add a folder to the "folders" list to enable the file watcher.')
        return False
    
    # If the watcher is enabled and there are folders, check that the folders exist.
    for folder in config_dict['watcher']['folders']:
        if not os.path.exists(folder):
            cuteprint(f'⚠️ The folder "{folder}" does not exist. Please check config.yaml.')
            return False

    # If the watcher is enabled, but no extensions are being watched, exit.
    if not config_dict['watcher']['extensions']:
        cuteprint('⚠️ No extensions are being watched in config.yaml. Add an extension to the "watched_extensions" list to enable the file watcher.')
        return False
    
    # If the watcher is enabled and there are extensions, check that the extensions are valid against the allowed extensions list.
    for ext in config_dict['watcher']['extensions']:

        # If the extension starts with a dot, remove it and update it in the config_dict too.
        if ext.startswith('.'):
            ext = ext[1:]
            config_dict['watcher']['extensions'][config_dict['watcher']['extensions'].index(ext)] = ext

        if ext not in ALLOWED_EXTS:
            cuteprint(f'⚠️ The extension "{ext}" is not supported. Please check config.yaml.')
            return False

    return True
