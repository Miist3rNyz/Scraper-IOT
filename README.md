# Scraper-IOT

# How to run the code ?

```bash
docker compose up
```

# What you want to know ?

The application need to perform an import of all CVEs (+237k) and most of the CPEs (+60k) from the NVD database.
Due to the limit of the NVD API, the application will be able to perform only 10 requests per minute.
This may impact the time of the first start of the application and the size of the database.
- First run time needed : ~30 min
- Database size : ~1 Go


# What you should not do ?

- Do not run the application without the docker-compose file, it may not work properly.
- Do not modify the file .metadata.json, it is used to store the last update date of the database.