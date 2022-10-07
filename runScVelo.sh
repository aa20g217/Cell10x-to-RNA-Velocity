papermill report1.ipynb report.ipynb -p fieName $1 -p basis $2 -p clusterFile $3 -p cellpath $4
jupyter nbconvert --no-input --to html report.ipynb
cp report.html ./figures/
