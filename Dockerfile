# base image
FROM continuumio/miniconda3

# project dependencies
RUN conda install pandas
RUN conda install seaborn
RUN conda install -c conda-forge scikit-learn
RUN conda install -c conda-forge matplotlib
RUN conda install -c conda-forge scikit-surprise
RUN conda install -c conda-forge flask
RUN conda install -c conda-forge keras

# create working directory
WORKDIR /app

# copy all the source files from current directory to docker
COPY . .

# expose port
EXPOSE 5000

# start the application
CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]

