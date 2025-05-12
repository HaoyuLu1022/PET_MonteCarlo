import os
import sys
import numpy as np
import configparser
import shutil
from distutils import util

# Command line arguments
patient_name = sys.argv[1]

if len(patient_name)==0:
    print('Please provide a patient name.')
    sys.exit()

# Directories
cur_dir = os.path.dirname(os.path.realpath(__file__))
config_dir = os.path.join(cur_dir, '../patients/configs/')

# Patient configuration
config = configparser.ConfigParser()
config.read(os.path.join(config_dir, patient_name+'.ini'))

# Determine phantom type
ph_type = config['Phantom']['type']
if 'vox' in ph_type:
    # Resolution of source phantom
    src_res = float(config['Phantom']['source_resolution'])
    # Resolution of attenuation phantom
    attn_res = float(config['Phantom']['attn_resolution'])
    
patient_dir = os.path.join(cur_dir, '../patients/', patient_name)
data_dir = os.path.join(patient_dir, 'phantom')

# Create directories
if not os.path.exists(patient_dir):
    os.mkdir(patient_dir)
if not os.path.exists(data_dir):
    os.mkdir(data_dir)

# Whether or not to perform reconstruction with JSRecon
recon = bool(util.strtobool(config['Reconstruction']['JSRecon']))

# Horizontal bed position
bed_pos = float(config['Setup']['bed_pos'])

# Duration of scan
scan_time = float(config['Simulation']['scan_time'])

if (ph_type.lower()=='nema_vox'):
    
    sys.path.append(os.path.join(cur_dir, 'nema'))
    from nema.generate_digital_nema import create_phantom, save_phantom, save_header, save_ranges, save_atten_map
    
    # Activity concentrations in Bq/mL
    sph_act = float(config['NEMA']['sph_act_conc'])
    bgnd_act = float(config['NEMA']['bgnd_act_conc'])
    
    # Create activity source
    phantom_size = np.array([int(200/src_res),int(400/src_res),int(400/src_res)])
    for i, p_z in enumerate(phantom_size):
        if p_z%2==0:
            phantom_size[i]+=1
    phantom = create_phantom(phantom_size=phantom_size,
                             dz=src_res, dy=src_res, dx=src_res, 
                             ph_type='act', spheres=True)
    # Save voxelized source
    save_phantom(phantom, data_dir, ph_type='act')
    # Save source info
    save_header(data_dir, phantom_size=phantom_size,
                dz=src_res, dy=src_res, dx=src_res, ph_type='act')
    # Save activity ranges
    save_ranges(data_dir, dz=src_res, dy=src_res, dx=src_res,
                sph_act=sph_act, bgnd_act=bgnd_act, ph_type='act')
    
    # Create attenuation phantom
    phantom_size = np.array([int(400/attn_res),int(400/attn_res),int(400/attn_res)])
    for i, p_z in enumerate(phantom_size):
        if p_z%2==0:
            phantom_size[i]+=1
    phantom = create_phantom(phantom_size=phantom_size,
                             dz=attn_res, dy=attn_res, dx=attn_res,
                             ph_type='attn', spheres=True)
    # Save voxelized phantom
    save_phantom(phantom, data_dir, ph_type='attn')
    # Save phantom info
    save_header(data_dir, phantom_size=phantom_size,
                dz=attn_res, dy=attn_res, dx=attn_res, ph_type='attn')
    # Save attenuation ranges
    save_ranges(data_dir, dz=attn_res, dy=attn_res, dx=attn_res, 
                sph_act=sph_act, bgnd_act=bgnd_act, ph_type='attn')
        
elif ph_type.lower()=='uniform_vox':
    
    sys.path.append(os.path.join(cur_dir, 'uniform_vox'))
    from uniform.generate_digital_uniform import create_phantom, save_phantom, save_header, save_ranges, save_atten_map
    
    # Activity concentrations in Bq/mL
    cyl_act = float(config['Uniform']['cyl_act_conc'])
    
    # Create activity source
    phantom_size = np.array([int(220/src_res),int(400/src_res),int(400/src_res)])
    for i, p_z in enumerate(phantom_size):
        if p_z%2==0:
            phantom_size[i]+=1
    phantom = create_phantom(phantom_size=phantom_size,
                             dz=src_res, dy=src_res, dx=src_res, 
                             ph_type='act', y_off=0, x_off=0, rot=0)
    
    # Save voxelized source
    save_phantom(phantom, data_dir, ph_type='act')
    # Save source info
    save_header(data_dir, phantom_size=phantom_size,
                dz=src_res, dy=src_res, dx=src_res, ph_type='act')
    # Save activity ranges
    save_ranges(data_dir, dz=src_res, dy=src_res, dx=src_res,
                cyl_act=cyl_act, ph_type='act')
    
    # Create attenuation phantom
    phantom_size = np.array([int(280/attn_res),int(400/attn_res),int(400/attn_res)])
    for i, p_z in enumerate(phantom_size):
        if p_z%2==0:
            phantom_size[i]+=1
    phantom = create_phantom(phantom_size=phantom_size,
                             dz=attn_res, dy=attn_res, dx=attn_res,
                             ph_type='attn', y_off=0, x_off=0, rot=0)
    # Save voxelized phantom
    save_phantom(phantom, data_dir, ph_type='attn')
    # Save phantom info
    save_header(data_dir, phantom_size=phantom_size,
                dz=attn_res, dy=attn_res, dx=attn_res, ph_type='attn')
    # Save attenuation ranges
    save_ranges(data_dir, dz=attn_res, dy=attn_res, dx=attn_res, 
                cyl_act=cyl_act, ph_type='attn')