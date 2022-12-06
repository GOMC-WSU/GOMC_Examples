{% extends "slurm.sh" %}

{% block header %}
{% set gpus = operations|map(attribute='directives.ngpu')|sum %}
    {{- super () -}}

{% if gpus %}
#SBATCH -q gpu
#SBATCH --gres gpu:{{ gpus }}
#SBATCH --constraint=v100
{%- endif %}

#SBATCH -N 1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --ntasks-per-core=1
#SBATCH --mail-type=END
#SBATCH --mail-user=xxx
#SBATCH -o output-%j.dat
#SBATCH -e error-%j.dat

echo  Running on host $HOSTNAME
date

source ~/.bashrc
conda activate mosdef2

#module load python/3.8
#module swap gnu7 intel/2019

{% if gpus %}
module load cuda/11.0
{%- endif %}

{% endblock header %}

{% block body %}
    {{- super () -}}


{% endblock body %}
