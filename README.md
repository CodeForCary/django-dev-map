# Code for America - Cary Django Site

This application takes [KML](https://developers.google.com/kml/) permit data 
issued by the towns of Cary and imports them into a 
[GeoDjango](http://geodjango.org/) application, which allows for native storage
of geometric objects and provides query tools for calculating region overlap, 
containment, etc. The app django exposes a simple API that supports such 
operations as:

- Rendering all permits into [GeoJSON](http://geojson.org/), suitable for 
  overlay on a map.
- Full-text search of the permit data.
- Retreving all permits that are present at a specific latitude/longitude.

A web interface is also included to allow exercising these APIs. 
The web interface leverages [AngularJs](https://angularjs.org/),
[Angular Material](https://material.angularjs.org/) and 
[Google Maps](https://developers.google.com/maps) to provide a seamless,
responsive UI targeted primarily toward a mobile user asking the question,
"What is being built here?".

## Architecture
The permit application is broken up into several pieces, with each part 
responsible for a different role. Each chunk, along with its major code entry
point are described below:

1. **Django Site**: Django encourages breaking up web apps into *sites* and 
   *applications*. The top level *site* in this repo is 'cfac'. The main 
   entry points are `cfac/settings.py` and `cfac/urls.py`. Other 
   than establishing basic functionality like database connections and 
   backend caches, the cfac site forwards to the permit\_map app.
2. **Django App**: The permit\_map application contains all of the logic for 
   importing, querying, and searching the permit data. Main entry points 
   here are in `permit_map/urls.py` and `permit_map/models.py`. The 
   permit\_map application also contains a single URL route (/) that renders
   the primary view: `permit_map/templates/permit_map/index.html`.
3. **AngularJS App**: The front-end is rendered using AngularJS. Angular is 
   invoked by the material.html template and control then shifts to a set of 
   statically served JavaScript and HTML files. All of the front-end code 
   comes from a CDN or is stored in `permit_map/static/permit_map/*`. The 
   main entry points are `js/app.js`, `js/controller.js`, and 
   `templates/material_map.html`.

## Local Development with Docker
Pulling down the source code and analyzing the various objects within the 
django shell is one of the fastest ways to understand how the applicaiton 
works. The primary mode of local development is to automatially provision
a local environment using [Docker](https://www.docker.com/).

Docker is a software suite that allows you to rapidly spin up development
environments. This git repo contains a set of "docker files" (see the 
./docker directory) that describes how the various components (django, 
database, etc.) of the dev map application are configured. Setting up an
environment is as easy as pulling the repo and issuing a few commands.
In theory anyway!

For a local deployment, you'll first need two primary components:

 - [Docker](https://docs.docker.com/installation/#installation) itself 
   will need to be installed.
 - [Docker Compose](http://docs.docker.com/compose/install/) needs to be
   installed on Linux and OS X machines.
 - Git also needs to be installed. On Windows, I recommend installing
   [Git Bash](http://git-scm.com/download/win) after you install docker.

A brief note about how Docker works on each platform is in order:

 - On **Linux**, docker runs as a system daemon and docker compose is a 
   first-class citizen. Everything runs natively and is extremely simple.
 - On **OS X**, as on Linux, docker and docker compose are native clients.
   But OS X does not support the virtual machines that docker uses to 
   build its systems (a.k.a. containers). Therefore, on OS X, the actual 
   virtual machines executing your code run inside a 
   [VirtualBox VM](https://www.virtualbox.org/). That's the 
   'boot2docker' part you'll see references to in the OS X install guide.
 - On **Windows**, none of these things are supported natively. Instead, 
   __everything__ runs inside the 'boot2docker' VM. Docker compose isn't 
   actually supported at all, so we do some magic tricks to make it all 
   work.

Once we get docker installed correctly, the commands are the same for 
every platform, but getting docker going can be a bit tricky. Here are
notes for the platforms that have been tested.

#### Linux

Follow the install guide on Docker's site. On Ubuntu, it's nice to be able
to run docker as a [non-root user](https://docs.docker.com/installation/ubuntulinux/#giving-non-root-access)

Otherwise, just clone the repo and step into it.

```
$ mkdir ~/projects
$ cd ~/projects
$ git clone https://github.com/CodeForCary/django-dev-map.git
```

#### OS X
<< TBD >>

#### Windows

The most complicated thing about Windows is figuring out what context you're
running in because you'll have (at some points) VMs inside of VMs inside of 
VMs ([seriously](https://www.virtualbox.org/)). Once you've got boot2docker 
and git bash installed, all you need to do is pull down this repo and log into 
the boot2docker VM.

```
$ mkdir ~/projects
$ cd ~/projects
$ git clone https://github.com/CodeForCary/django-dev-map.git
$ boot2docker download
$ boot2docker init
$ boot2docker start
$ boot2docker ip    <-- jot this down for future reference
$ boot2docker ssh
docker$ cd /c/Users/<< your user name >>/projects/django-dev-map
docker$ . docker/windows-init
```

At the end of this, you are running commands inside the boot2docker VM, but 
you are actually looking at your Windows home directory. So if you edit the 
code here, you'll change the application.

The last command above, where we source in the 'windows-init' file, is what 
allows us to use docker compose on Windows.

#### Configuring the Dev Map App

Now that docker is installed and our repo is checked out, we're ready to get
the dev map application up and running. Let's start by executing Django's 
management script __via Docker__. So this command will spin up a virtual 
machine and run the command in that context:

```
chmod +x *.sh *.py
./dmanage.sh --help
```

You'll probably want to go get a cup of coffee, because this will be the 
longest that you've ever waited for a help screen. Running dmanage for the 
first time provisions:

 - A postgres database, with the postgis extensions installed
 - A python environment capable of running our django application
 - An npm/bower environment with all of our Javascript dependencies

You can see all of these described in the __docker-compose.yml__ file at the 
root of the repository. Once all these containers have been built, and 
assuming there are no errors, you should get the help screen for Django.

Next, we need to set up our database:

```
./dmanage.sh schemamigration permit_map --init
./dmanage.sh syncdb
./dmanage.sh migrate permit_map
```

These three commands:

 1. Calculate the set of SQL to run to create our initial tables for 
    the permit_map application.
 2. Create the basic tables/structures for Django.
 3. Apply the SQL calculated in step #1.

We now have a database in our postgres docker container. Lets import some 
permit data into that database:

```
./dimport.sh --town Cary shapefiles/cary/*.kml
```

Once this command finishes, all shapefile data has been imported and we're
ready to bring our application up for the first time. Execute:

```
docker-compose up
```

This should spin up all the containers and you can now view the app in your
browser:

```
http://<< ip address >>:8080/
```

The IP address will differ depending on your platform:

 - On **Linux** it's the IP address of your machine.
 - On **OS X** it's...I think it's your machine's IP.
 - On **Windows** it's the ip address that you noted earlier when you 
   ran ``boot2docker ip``.

You should now be able to edit both Python and Javascript files and see 
your changes by simply refreshing the browser window. You can bring 
everything down just by hitting CTRL-C.
