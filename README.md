# elxr-config

## Introduction

This project provides stock configuration manifests for building Linux images
using Rucksack and Tiler tools. With these manifests you can create the
following image types:

* Base images - standard root filesystems
* VM images - ex. installer, minimal, AI
* Cloud images - ex. Azure, EC2
* Board specific images - ex. Orin, IMX
* Container images

## Manifest format

### Image manifest

The image manifest defines the name, description, architecture, version and so
on for an image. Each image manifest can be used for building an image.
Typically there are two image manifests in each directory, for example in
vm/minimal/:

* image-ostree.yaml: The ostree image
* image.yaml: The image without ostree

You can use the following command to find all the image manifests:

```bash
  $ find . -name 'image*.yaml'
```

And use Rucksack to build them:

```bash
  $ rs build --debug --config path/to/image-ostree.yaml
  $ ls *.img *.img.zst
```

Review the README.md in the Rucksack repository for more details on "rs build"

### Package manifest fragment

The package manifest fragment lists the packages which are to be installed to
the image. They are part of a "Image manifest", for example in
vm/xfce4/image-ostree.yaml we have:

  ```yaml
  packages:
    - ${include:manifests/packages-ostree.yaml}
    - ${include:manifests/packages-xfce4.yaml}
  ```

Which means that packages in manifests/packages-ostree.yaml and
manifests/packages-xfce4.yaml will be installed in the resulting image.

## Create your own manifest

1. Copy minimal directory as a start point

   ```bash
     $ cp -a vm/minimal my-image
   ```

   You can use other preferred names to replace my-image.
1. Customize my-image
   There are two image manifests in my-image directory:
   * image-ostree.yaml: The ostree image
   * image.yaml: The image without ostree

   The two manifests are independent, you can keep the one you need, and remove
   the other one. Here we use image-ostree.yaml as an example. Open
   image-ostree.yaml and edit it as needed. For example, edit name, description,
   architecture and version, and also edit the "packages" section to include
   more packages, you can use manifest fragments from the manifests directory:

    ```yaml
      packages:
      - ${include:manifests/packages-ostree.yaml}
      - ${include:manifests/packages-xfce4.yaml}
    ```

   Or add the packages directly:

    ```yaml
      packages:
      - ${include:manifests/packages-ostree.yaml}
      - task-xfce-desktop
      - network-manager-gnome
    ```

1. Build Customized image

   ```bash
    $ rs build --debug --config path/to/my-image/image-ostree.yaml
   ```

   Review the README.md in the Rucksack repository for more details on "rs build"
