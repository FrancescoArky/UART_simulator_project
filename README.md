For the proper functioning of the project it has been necessary to use as well the VSPE software (https://eterlogic.com/Products.VSPE.html). After having downloaded it, it has been necessary to perform the following steps:

- Device -> create -> Connector: Pair -> Choose COM1 and COM2 along with the option "Emulate Baud Rate"

- On the main page select "Start emulation" and "Start/Stop HTTP Server"

- Run main.py


The .exe file is located inside the "dist" folder


In order to build the docker file it is necessary to follow the instructions below:

1. Make sure to be in the simulatore-seriale folder, then write the following command:

    docker build -t simulatore_arcamone_image .

If the image has been built correctly you should find it through the command:

    docker images

2. Create a container based on that image through the command:

    docker run --name simulatore_arcamone_container simulatore_arcamone_image

3. Run the image within the container with this command:

    docker run --name simulatore_arcamone_container simulatore_arcamone_image
