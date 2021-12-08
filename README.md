fingernat-pymol-plugin
============

<!-- TOC START min:1 max:6 link:true asterisk:false update:true -->
- [About](#about)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Contributors](#contributors)
<!-- TOC END -->



# About

![logo_fingernat](logo_fingernat160.png)

This PyMOL plugin visualizes interactions detected by the [fingeRNAt progam](https://github.com/n-szulc/fingeRNAt/). This means that you need to run it first and generate data to be visualized in this plugin. But don't worry, it's quite simple :)

This plugin works with PyMOL 2.x and Python 3.

<!-- markdown-link-check-disable-next-line -->
[![Check Markdown links](https://github.com/filipsPL/fingernat-pymol-plugin/actions/workflows/action-links.yml/badge.svg)](https://github.com/filipsPL/fingernat-pymol-plugin/actions/workflows/action-links.yml)

# Installation

<!-- markdown-link-check-disable-next-line -->
In PyMOL window go to top menu - Plugin manager - Install new plugin - paste *https://github.com/filipsPL/fingernat-pymol-plugin* in the URL field, click `Fetch`:

![](obrazki/README-3b91eee4.png)

The fingeRNAt plugin will be available from the Plugin menu:

![](obrazki/README-ded6536c.png)


# Usage

1. Load into PyMOL nucleic acid and ligand structures you had used to detect interactions with the fingeRNAt.

2. Open the fingeRNAt plugin, click Browse and point to the DETAIL_... tsv file which was generated by fingeRNAt.

3. Click `Proceed!`

![](obrazki/README-5b762be2.png)

4. A bunch of new groups and objects are created:

![](obrazki/README-851e9a88.png)

- Interactions: objects holding detected interactions. The exact number depends of the detected inteactions types.
- Receptor preferences: objects showing preferences of the receptor for forming/accomodating the given type of interaction.
- Ligand preferences: objects showing preferences of the ligand binding pocket for forming/accomodating the given type of interaction.
- Neighbours: fragment of the receptor containing residues which form interactions with ligand

Each group and object can be hidden/shown separately.

5. Each ligand's model (state) contains interactions detected for this particular model. The last model (state) contains the visual legend of the detected interactions:

![](obrazki/README-777f64f7.png)


Additionally, the color codes are printed in the console:

```
---------- Colors legend: -----------
  Hydrogen bond (HB) is presented in marine
  Cation-anion (CA) is presented in red
  Halogen bond (HAL) is presented in purple
  Lipophilic (Lipophilic) is presented in silver
  Pi-stacking (Pi_Stacking) is presented in orange
  Pi-cation (Pi_Cation) is presented in green
  Pi-anion (Pi_Anion) is presented in hotpink
  Water-mediated (Water-mediated) is presented in blue
  Ion-mediated (Ion-mediated) is presented in salmon
  any_contact (any_contact) is presented in teal
```

# Screenshots


| pymol                            | description                                                                    |
| -------------------------------- | ------------------------------------------------------------------------------ |
| ![](obrazki/README-65a8be8a.png) | Overview of the formed interactions                                            |
| ![](obrazki/README-8890c249.png) | Receptor preferences                                                           |
| ![](obrazki/README-e95e087b.png) | Ligand preferences in the ligand binding site                                 |
| ![](obrazki/README-2765c99c.png) | Preferred positions of Pi-involving interactions and cation anion-interactions |
| ![](obrazki/README-1945eb54.png) | As above, but for the receptor                                                 |
| ![](obrazki/README-e481bf7b.png) | User defined interactions; some bonds are heading to implicit hydrogens        |


# Contributors

| :octocat:       | github                                   | contact                                                                  |
| --------------- | ---------------------------------------- | ------------------------------------------------------------------------ |
| Filip Stefaniak | [@filipsPL](https://github.com/filipsPL) | ![](https://img.shields.io/badge/fstefaniak-%40iimcb.gov.pl-brightgreen) |
| Natalia Szulc   | [@n-szulc](https://github.com/n-szulc)   | ![](https://img.shields.io/badge/nszulc-%40iimcb.gov.pl-brightgreen)     |
