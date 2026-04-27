#!/bin/bash
#SBATCH --job-name=hp_acopf
#SBATCH --output=/home/g202210120/Homeomorphic-Projection/logs/hp_acopf_%j.out
#SBATCH --error=/home/g202210120/Homeomorphic-Projection/logs/hp_acopf_%j.err
#SBATCH --time=24:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --partition=gpu_x450
#SBATCH --gres=gpu:1
#SBATCH --chdir=/home/g202210120/Homeomorphic-Projection

set -e

source $(conda info --base)/etc/profile.d/conda.sh
conda activate bispro

echo "Running on node: $(hostname)"
echo "Working directory: $(pwd)"
echo "CUDA_VISIBLE_DEVICES: $CUDA_VISIBLE_DEVICES"
echo "Python path: $(which python)"
echo "Starting training_all.py"

python -u training_all.py

echo "Finished training_all.py"