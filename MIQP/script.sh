#!/bin/bash
#SBATCH --job-name="Taxis"
#SBATCH --partition=general
#SBATCH -n 1 # particiones
#SBATCH -c 20 # cores
#SBATCH --output=resultados.out
#SBATCH --error=fail.error
#SBATCH --mail-user=luis.rojo.g@usach.cl
#SBATCH --mail-type=ALL
#SBATCH --mem-per-cpu=10000

#Variables, rutas y módulos
echo $SLURM_ARRAY_TASK_ID;
echo "SLURM_JOBID="$SLURM_JOBID
echo "SLURM_JOB_NODELIST"=$SLURM_JOB_NODELIST
echo "SLURM_NNODES"=$SLURM_NNODES
echo "SLURMTMPDIR="$SLURMTMPDIR
echo "working directory="$SLURM_SUBMIT_DIR

srun --export=ALL ./ejecutable.o servicios.txt disponibilidades.txt vehiculos.txt bases.txt tipos.txt anterior.txt
echo "Trabajo terminado"
