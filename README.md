# handtos.mochisuke.jp based on tos.guru
A fan-made and open-source Database & Simulator for Tree of Savior, an MMORPG being developed by IMCGAMES CO., LTD.
Includes iTOS, jTOS, kTOS and kTEST regions.
Converted and modified by ebisuke[https://handtos.mochisuke.jp]
based on [https://tos.guru](https://tos.guru)

* How to launch 
1. Create `tos` user in the host computer.
```
sudo useradd -u 10001 -g 10001 tos
```
2..Create `.env` file and specity uid,gid.
```
LOCAL_UID=10001
LOCAL_GID=10001

```

3. Execute `docker-compose`.
```
docker-compose build && docker-compose up 
```

it will expose port 8000 as http.