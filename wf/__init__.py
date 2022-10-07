"""
A worflow to obtain the pre-mature (unspliced) and mature (spliced) transcript information using cellranger sample folder, followed by RNA-velocity analysis.
"""


import subprocess
from pathlib import Path

from flytekit import LaunchPlan, workflow
from latch.types import LatchDir,LatchFile
from latch import large_task
from latch.resources.launch_plan import LaunchPlan
from latch.resources.reference_workflow import workflow_reference
import os,glob, shutil

@large_task
def runVelocyto(inputDir: LatchDir,output_dir: LatchDir,gtfFile: LatchFile,maskFile: LatchFile,clusterFile:LatchFile,embedding: str="umap") -> LatchDir:
    os.mkdir('/root/tempDir')

    if maskFile.remote_path==LatchFile("latch:///"):
        maskFile=""

    if clusterFile.remote_path==LatchFile("latch:///"):
        clusterFile=""


    if maskFile=="":
        #subprocess.run(
        _cmd=[
                "velocyto",
				"run10x",
                inputDir.local_path,
                gtfFile.local_path
            ]
        #)
    else:
        #subprocess.run(
        _cmd=[
                "velocyto",
				"run10x",
                "-m",
                maskFile.local_path,
                inputDir.local_path,
                gtfFile.local_path
            ]
        #)


    with open("/root/tempDir/log.txt", "w") as f:
        subprocess.call(_cmd, stdout=f)

    with open('/root/tempDir/log.txt') as f:
        lines = f.readlines()
        for line in lines:
	        if '.loom' in line:
	            path=line.split(" ")[-1][:-1]
	            print(path)
	            break

    shutil.copy2(path, '/root/tempDir/velocytoOutput.loom')

    if clusterFile=="":
        clusterFile="None"
    else:
        clusterFile=clusterFile.local_path

    subprocess.run(
        [
            "sh",
            "runScVelo.sh",
            '/root/tempDir/velocytoOutput.loom',
			embedding,
            clusterFile,
			inputDir.local_path
        ]
    )

    shutil.move("/root/figures", "/root/tempDir/")


    local_output_dir = str(Path("/root/tempDir/").resolve())
    remote_path=output_dir.remote_path
    if remote_path[-1] != "/":
       remote_path += "/"

    return LatchDir(local_output_dir,remote_path)


@workflow
def velocyto_wf(inputDir: LatchDir,output_dir: LatchDir,gtfFile: LatchFile,maskFile: LatchFile,clusterFile: LatchFile,embedding: str="umap") -> LatchDir:
    """

    Cell10x-to-RNA-Velocity.
    ----

    A worflow to obtain the pre-mature (unspliced) and mature (spliced) transcript information using cellranger sample folder, followed by RNA-velocity analysis. `RNA velocity analysis`  allows us to infer transcriptional dynamics that are not directly observed in a scRNA-seq experiment using a mathematical model of transcriptional kinetics. We can use RNA velocity to determine if a gene of interest is being induced or repressed in a give cell population of interest. Moreover, we can extrapolate this information to predict cell fate decision via pseudotime trajectories.

    __metadata__:
        display_name: Cell10x-to-RNA-Velocity..
        author:
            name: Akshay
            email: akshaysuhag2511@gmail.com
            github:
        repository:
        license:
            id: MIT

    Args:

        inputDir:
          The Cell Ranger output directory, which contains the subfolders outs, outs/analysis, etc. Make sure you have unzipped the zipped file in the given directory.

          __metadata__:
            display_name: cellranger sample folder

        gtfFile:
          A genome annotation (GTF file). This needs to be the same GTF in the reference used to run Cell Ranger or durig the allignment.

          __metadata__:
            display_name: GTF file

        maskFile:
          A .gtf file containing intervals to mask expressed repetitive elements, since those count could constitute a confounding factor in the downstream analysis.

          __metadata__:
            display_name: Mask file

        clusterFile:
          A .csv file where the first column will be barcode and the second column will be cell type. In the absence of this file, clustering information from cell10x will be used.

          __metadata__:
            display_name: Cell Types

        embedding:
          	Possible options are umap,tsne, and pca.

          __metadata__:
            display_name: Embedding Type

        output_dir:
          Where to save the report and plots?.

          __metadata__:
            display_name: Output Directory
    """
    return runVelocyto(inputDir=inputDir,gtfFile=gtfFile,maskFile=maskFile,clusterFile=clusterFile,embedding=embedding,output_dir=output_dir)

LaunchPlan(
    velocyto_wf,
    "Test Data",
    {
		#"inputDir": LatchFile("s3://latch-public/test-data/4148/cell10xOutput_new/outs/cellsorted_possorted_genome_bam.bam"),
        "gtfFile": LatchFile("s3://latch-public/test-data/4148/gencode.v32.primary_assembly.annotation.gtf"),
        "maskFile": LatchFile("s3://latch-public/test-data/4148/mm10_rmsk.gtf"),
		"clusterFile": LatchFile("s3://latch-public/test-data/4148/velocyto/3p-Neutrophils-clusters.csv")

    },
)
