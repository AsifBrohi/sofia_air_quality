<a name="readme-top"></a>

# **Sofia, Bulgaria Monthly Air Quality Data**

**Table of contents**

- [Project Background](#project-background)
- [Devlopment Roadmap](#development-roadmap)

## Project Background
Approached by client as they have got Sofia, Bulgaria air quality data. This data is in CSV format, monthly data which contains sensor_id, location, lattidue, longitudinal, timestamp, pressure, temp, humidity. Currently the data is just stored in CSV files client wants to extract the file from kaggle place it into cloud storage in CSV format. From Cloud storage extract the CSV file make minor transformations and load it into Bigquery. 
Client wanted to see the changes in air quality through-out the month in Sofia Bulgaria. 

## Development Roadmap 
### Week 1 
#### Extract CSV File 
```python

def extract(file_name :str,download_dir :str) -> None:
    """extracting csv file from kaggle"""
    try:
        path_zip_csv = os.path.join(download_dir,file_name+".zip")
        os.system(f"kaggle datasets download -d  hmavrodiev/sofia-air-quality-dataset -f {file_name} -p {download_dir} ")
        print(f"{file_name} has been downloaded")
        with zipfile.ZipFile(path_zip_csv,'r') as unzip_csv:
            unzip_csv.extractall(download_dir)
            print("Unzipped File")
    except FileNotFoundError as error:
        print(error)
        print("File Not Found")
    except FileExistsError as file_exist:
        print(file_exist)
        print("file already exist")


```
#### Docker & PostgreSQL
Create a docker-compose.yaml file. First image being postgreSQL configuration and Second image adminer which is dependent on first image.
```yaml
version: '3.1'
services:
  db:
      image: postgres:13
      container_name: sofia_air_quality
      restart: always
      environment:
        POSTGRES_USER: root
        POSTGRES_PASSWORD: root
        POSTGRES_DB: sofia_air_qty
      ports:
        - "5432:5432"
      volumes:
        - ./sofia_air_quality_data:/var/lib/postgresql/data
  adminer:
        image: adminer
        container_name: visual_adminer
        depends_on:
          - db
        restart: always
        environment:
          ADMINER_DEFAULT_DB_DRIVER: PostgreSQL
          ADMINER_DEFAULT_DB_HOST: db
          ADMINER_DEFAULT_DB_NAME: sofia_air_qty
        ports:
          - "8080:8080"

```
