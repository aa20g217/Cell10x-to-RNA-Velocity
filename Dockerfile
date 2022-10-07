FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:9a7d-main

#install samtools
RUN apt-get update -y &&\
 apt-get install -y autoconf samtools

# Install pip
RUN apt-get install -y python3-pip

#install required packages
RUN python3 -m pip install -U scvelo
RUN python3 -c "import scvelo"

RUN python3 -m pip install -U jupyter notebook
RUN jupyter notebook --version

RUN python3 -m pip install -U papermill
RUN python3 -c "import papermill"

RUN python3 -m pip install -U black
RUN python3 -c "import black"

RUN python3 -m pip install -U numpy
RUN python3 -c "import numpy"

RUN python3 -m pip install -U scipy
RUN python3 -c "import scipy"

RUN python3 -m pip install -U cython
RUN python3 -c "import cython"

RUN python3 -m pip install -U numba
RUN python3 -c "import numba"

RUN python3 -m pip install -U matplotlib
RUN python3 -c "import matplotlib"

RUN python3 -m pip install -U scikit-learn
RUN python3 -c "import sklearn"

RUN python3 -m pip install -U h5py
RUN python3 -c "import h5py"

RUN python3 -m pip install -U click
RUN python3 -c "import click"

RUN python3 -m pip install -U velocyto
RUN velocyto --help

# You can use local data to construct your workflow image.  Here we copy a
COPY report1.ipynb /root/report1.ipynb
COPY runScVelo.sh /root/runScVelo.sh


# STOP HERE:
# The following lines are needed to ensure your build environement works
# correctly with latch.
COPY wf /root/wf
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
RUN python3 -m pip install --upgrade latch
WORKDIR /root
