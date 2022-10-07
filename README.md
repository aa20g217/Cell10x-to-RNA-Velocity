# RNA velocity analysis
### **Summary**
RNA velocity analysis allows us to infer transcriptional dynamics that are not directly observed in a scRNA-seq experiment using a mathematical model of transcriptional kinetics. We can use RNA velocity to determine if a gene of interest is being induced or repressed in a give cell population of interest. Moreover, we can extrapolate this information to predict cell fate decision via pseudotime trajectories.

Here I have developed a worflow to obtain the pre-mature (unspliced) and mature (spliced) transcript information using cellranger sample folder, followed by RNA-velocity analysis.


### **Input**

###### Cellranger sample folder
The Cell Ranger output directory, which contains the subfolders outs, outs/analysis, etc. Make sure you have unzipped the zipped file in the given directory. Example input directory: https://console.latch.bio/s/267594166506436. You can get an example input file for all the remaining parameters by using the load test data feature of the latch.

###### GTF file
 A genome annotation (GTF file). This needs to be the same GTF in the reference used to run Cell Ranger or durig the allignment. 

###### Mask file
A .gtf file containing intervals to mask expressed repetitive elements, since those count could constitute a confounding factor in the downstream analysis.


###### Cell Types
A .csv file where the first column will be barcode and the second column will be cell type. In the absence of this file, clustering information from cell10x will be used.


###### Embedding Type
Possible options are umap,tsne, and pca.

### **Output**
An HTML report with RNA velocity analysis results. In addition, a folder with publication-ready plots.

### **Latch wf link**
https://console.latch.bio/explore/82196/info

