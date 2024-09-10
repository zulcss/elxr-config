# Introduction
These are stock configuration for both Rucksack and Tiler. These manifests will create the following:

* rootfs tarball
* ostree rootfs tarball
* Stock amd64/arm64 images
* Stock amd64/arm64 images with ostree.

# Manifest format
## Image manifest
The image manifest defines name, description, architecture version and so on for an image, each
image manifest can be used for building an image, usually, there two image manifests in each
directory, for example, vm/minimal/:

* image-ostree.yaml: The ostree image
* image.yaml: The image without ostree

You can use the following command to find all image manifests:

$ find . -name 'image*.yaml'

And use rucksack to build them:

```
    $ rs --debug build --config path/to/image-ostree.yaml
    $ ls *.img *.img.zst
```

Check README in rucksack repository to see more details for "rs build"

## Package manifest fragment
The package manifest fragment lists the packages which are needed to installed to the image, they
are part of a "Image manifest", for example, in vm/xfce4/image-ostree.yaml:

        packages:
          - ${include:manifests/packages-ostree.yaml}
          - ${include:manifests/packages-xfce4.yaml}

Which means that packages in manifests/packages-ostree.yaml and manifests/packages-xfce4.yaml will
be installed to xfce4/image-ostree.yaml.

# Create your own manifest
1. Copy minimal directory as a start point

    $ cp -a vm/minimal my-image

    You can use other preferred names to replace my-image.

2. Customize my-image
    There are two image manifests in my-image directory:
    * image-ostree.yaml: The ostree image
    * image.yaml: The image without ostree

    The two manifests are independent, you can keep the one you need, and remove the other one. Use
    image-ostree.yaml as an example here, open image-ostree.yaml and edit it as needed, for example,
    edit name, description, architecture and version, and also edit the "packages" section to
    include more packages, you can use manifest fragment from the manifests directory:

        packages:
          - ${include:manifests/packages-ostree.yaml}
          - ${include:manifests/packages-xfce4.yaml}

    Or add the packages directly:

        packages:
          - ${include:manifests/packages-ostree.yaml}
          - task-xfce-desktop
          - network-manager-gnome

3. Build Customized image

    $ rs --debug build --config path/to/my-image/image-ostree.yaml

    Check README in rucksack repository to see more details for "rs build"
