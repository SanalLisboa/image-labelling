PYTHON VERSION

    `python: 3.8.0`


RUNNING APP WITHOUT DOCKER

    `cd <PROJECT ROOT DERICTORY>`
    `pip install -r requirements.txt`
    `mkdir <image-storage-path>`
    `export POSTGRES_DBNAME=<POSTGRES_DBNAME>`
    `export POSTGRES_DBUSER=<POSTGRES_DBUSER>`
    `export POSTGRES_DBPASSWORD=<POSTGRES_DBPASSWORD>`
    `export POSTGRES_DBHOST=<POSTGRES_DBHOST>`
    `export POSTGRES_DBPORT=<POSTGRES_DBPORT>`
    `export TEMP_FILE_STORAGE_PATH=<image-storage-path>`
    `python manage.py migrate`
    `python manage.py runserver`


REQUIREMENTS TO RUN THE PROJECT USING DOCKER

    `docker: 20.10.8`
    `docker-compose: 1.29.2`

Note: The docker compose file included should be used for testing purpose only not intended for production.


RUNNING PROJECT WITH DOCKER

    `cd <PROJECT ROOT DERICTORY>`
    `docker-compose up`


API SPECS

Import `image-labelling-spec.yml` in Insomnia app


IDEAL API FLOW

![Alt text](readme_static/api-flow.png?raw=true "Image lebelling API flow")


DEPLOYMENT

    * Amazon Web Services:
        * Services Required:
            1. EC2 Instance: t3a.small
            2. Amazon EBS volume: 20GB
            3. Application Load Balancer
            4. AWS Auto Scaling

    * CI/CD:
        * jenkins: UI interface to manage deployments
        * ansible: Automate deployments


DEPLOYMENT FLOW

![Alt text](readme_static/deployment.png?raw=true "Deployment flow")


AWS SETUP(With load balancing and downtime prevention)

![Alt text](readme_static/aws-setup.png?raw=true "AWS Setup")


Note: The images are rightnow stored in file system but better solution will be storing it on cloud on s3. 