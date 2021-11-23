'''
pymol plugin for displaying data from fingernat analysis
generate output file first using option -detail

plugin by Filip Stefaniak, fstefaniak@iimcb.gov.pl

please note: this code is Python3!

# may be necesary to install pandas:
# python3 -m pip install pandas
'''


from __future__ import absolute_import
from __future__ import print_function

# Avoid importing "expensive" modules here (e.g. scipy), since this code is
# executed on PyMOL's startup. Only import such modules inside functions.

import os
from pymol.cgo import *


def __init_plugin__(app=None):
    '''
    Add an entry to the PyMOL "Plugin" menu
    '''
    from pymol.plugins import addmenuitemqt
    addmenuitemqt('fingeRNAt Visualization', run_plugin_gui)


# global reference to avoid garbage collection of our dialog
dialog = None


def run_plugin_gui():
    '''
    Open our custom dialog
    '''
    global dialog

    if dialog is None:
        dialog = make_dialog()

    dialog.show()

def make_dialog():
    # entry point to PyMOL's API
    from pymol import cmd

    # pymol.Qt provides the PyQt5 interface, but may support PyQt4
    # and/or PySide as well
    from pymol.Qt import QtWidgets
    from pymol.Qt.utils import loadUi

    # create a new Window
    dialog = QtWidgets.QDialog()

    # populate the Window from our *.ui file which was created with the Qt Designer
    # launch with: designer
    uifile = os.path.join(os.path.dirname(__file__), 'fingerwidget.ui')
    form = loadUi(uifile, dialog)


    def readFormCheckBoxesValues(form):
        # just return config values from dialog
        return [form.checkBox_ReceptorPreferences.isChecked(),
                        form.checkBox_LigandPreferences.isChecked(),
                        form.spinBox_transparency.value(),
                        form.newObjectsPrefix.text(),
                        form.checkBox_neighbours.isChecked()]

    def deleteFNobjects():
        # remove fingernat created objects
        print("Removing all fingeRNAt objects...")
        cmd.delete("*Interactions")
        cmd.delete("*ReceptorPreferences")
        cmd.delete("*LigandPreferences")
        cmd.delete("*Legends")
        cmd.delete("*fingernat")
        cmd.delete("neighbours")
        cmd.delete("%neighbours")

    def loadSampleFile():
        # checkboxes
        configFromForm = readFormCheckBoxesValues(form)

        currentDir = os.path.dirname(__file__)

        cmd.load(currentDir + "/sample_data/ligands.sdf", "ligands")
        cmd.load(currentDir + "/sample_data/rna.pdb", "RNA")
        parseFile(currentDir + "/sample_data/DETAIL_FULL.tsv", configFromForm, form)
        cmd.orient("RNA")

    # callback for the "proceed/run" button
    def run():
        filename = form.input_filename.text()

        # checkboxes
        configFromForm = readFormCheckBoxesValues(form)

        if filename:
            parseFile(filename, configFromForm, form)
        else:
            print('Please select or enter the filename')

    # callback for the "Browse" button
    def browse_filename():
        filename = QtWidgets.QFileDialog.getOpenFileName(
            dialog, 'Open DETAIL file', filter='fingeRNAt TSV files (DETAIL_*.tsv);;TSV files (*.tsv *.csv);;Text files (*.txt);;All files (*)')[0]
        if filename:
            form.input_filename.setText(filename)


    # hook up button callbacks
    form.button_proceed.clicked.connect(run)
    form.button_sample.clicked.connect(loadSampleFile)
    form.button_browse.clicked.connect(browse_filename)
    form.button_close.clicked.connect(dialog.close)
    form.button_remove.clicked.connect(deleteFNobjects)

    return dialog

def parseFile(file, configFromForm, form):

    import pandas as pd
    from collections import OrderedDict
    from pymol import cmd

    cmd.set("group_auto_mode", 2) #Treats dots in object names as group prefix delimiter. 0: off, 1: put in existing groups, 2: create groups if they do not exist

    # assing values from the form data
    checkBox_ReceptorPreferences = configFromForm[0]
    checkBox_LigandPreferences = configFromForm[1]
    cgo_transparency = configFromForm[2] / 100 # scaling to 0.0 - 1.0 range
    newObjectsPrefix = configFromForm[3].strip()

    if(newObjectsPrefix != ''):
        print("jest niepusty")
    else:
        print("pusty")

    interactionColors = OrderedDict()
    interactionColors['HB'] = "marine"
    interactionColors['CA'] = "red"
    interactionColors['HAL'] = "purple"
    interactionColors['Lipophilic'] = "silver"
    interactionColors['Pi_Stacking'] = "orange"
    interactionColors['Pi_Cation'] = "green"
    interactionColors['Pi_Anion'] = "hotpink"
    interactionColors['Water-mediated'] = "blue"
    interactionColors['Ion-mediated'] = "salmon"


    interactionDashWidth = {}
    interactionDashWidth['Pi_Stacking'] = 2
    interactionDashWidth['Pi_Cation'] = 2
    interactionDashWidth['HB'] = 2
    interactionDashWidth['CA'] = 2
    interactionDashWidth['Pi_Anion'] = 2
    interactionDashWidth['HAL'] = 2
    interactionDashWidth['Water-mediated'] = 0.5
    interactionDashWidth['Ion-mediated'] = 0.5
    interactionDashWidth['Lipophilic'] = 2


    interactionDashGap = {}
    interactionDashGap['Pi_Stacking'] = 0.01
    interactionDashGap['Pi_Cation'] = 0.01
    interactionDashGap['Pi_Anion'] = 0.01
    interactionDashGap['HB'] = 0.5
    interactionDashGap['CA'] = 0.5
    interactionDashGap['HAL'] = 0.5
    interactionDashGap['Water-mediated'] = 0.08
    interactionDashGap['Ion-mediated'] = 0.08
    interactionDashGap['Lipophilic'] = 0.5

    interactionDesc = {}
    interactionDesc['Pi_Stacking'] = "Pi-stacking"
    interactionDesc['Pi_Cation'] = "Pi-cation"
    interactionDesc['HB'] = "Hydrogen bond"
    interactionDesc['CA'] = "Cation-anion"
    interactionDesc['Pi_Anion'] = "Pi-anion"
    interactionDesc['HAL'] = "Halogen bond"
    interactionDesc['Water-mediated'] = "Water-mediated"
    interactionDesc['Ion-mediated'] = "Ion-mediated"
    interactionDesc['Lipophilic'] = "Lipophilic"

    #
    # parameters for non-hardcoded interactions (from custom plugin):
    #

    # colors to use for new, not hardcoded interactions

    interactionColorsOther = ['teal', 'limegreen', 'darksalmon', 'nitrogen', 'warmpink', 'lightpink', 'deepteal', 'raspberry', 'oxygen', 'deeppurple', 'skyblue', 'carbon', 'purpleblue', 'olive', 'lightteal', 'smudge', 'chocolate', 'greencyan', 'deepblue', 'lightmagenta', 'magenta', 'palecyan', 'hydrogen', 'palegreen', 'tv_blue', 'tv_green', 'pink', 'gray', 'ruby', 'chartreuse', 'sulfur', 'yellow', 'splitpea', 'limon', 'deepolive', 'paleyellow', 'dash', 'white', 'wheat', 'density', 'sand', 'violet', 'forest', 'yelloworange', 'lightblue', 'firebrick', 'lightorange', 'violetpurple', 'tv_orange', 'tv_red', 'lime', 'slate', 'deepsalmon', 'deepsalmon', 'grey', 'cyan', 'brightorange', 'tv_yellow', 'dirtyviolet', 'brown', ]


    interactionDashWidthOther = 0.5
    interactionDashGapOther = 0.03


    #

    # is this line slow? check on the large structures - checkbox: checkBox_neighbours
    neighboursSelector = "((br. all within 2 of pseudo1) or (br. all within 2 of pseudo2)) and (polymer.nucleic or metals or resn HOH)"

    sampleFileName = file

    interactionData = pd.read_csv(sampleFileName, delimiter="\t")

    interactionDataGrouped = interactionData.groupby(['Ligand_name', 'Ligand_pose'])
    interactionDataGroupedLen = len(interactionDataGrouped)


    form.progressBar.setTextVisible(True)
    form.label_15.setText("Loading structures...")

    state = 0
    for i, (name, group) in enumerate(interactionDataGrouped):
        # ligandPoseName="^".join( [str(x) for x in name ] )
        # print(ligandPoseName)
        state = i+1
        form.progressBar.setValue( int(state/interactionDataGroupedLen*100) )

        # group.sort_values(by=['Ligand_pose'], inplace=True)

        for row in group.iterrows():
            _, Ligand_name, Ligand_pose, Ligand_occurrence_in_sdf, Interaction, Ligand_Atom, Ligand_X, Ligand_Y, Ligand_Z, \
                Receptor_Residue_Name, Receptor_Number, Receptor_Chain, Receptor_Atom, \
                Receptor_X, Receptor_Y, Receptor_Z, Distance = row[1]

            cmd.pseudoatom("pseudo1", pos=[Ligand_X, Ligand_Y, Ligand_Z], state=Ligand_occurrence_in_sdf)
            cmd.pseudoatom("pseudo2", pos=[Receptor_X, Receptor_Y, Receptor_Z], state=Ligand_occurrence_in_sdf)
            cmd.distance( "Interactions.Inter--%s" % (Interaction), "pseudo1", "pseudo2")
            cmd.hide("labels", "Interactions.Inter--%s" % (Interaction) ) # hide distance of the interaction

            cmd.select("neighbours", neighboursSelector, merge=1)
            # cmd.select("neighbours", "(br. all within 2 of pseudo2) and polymer.nucleic", merge=1)

            cmd.delete("pseudo1")
            cmd.delete("pseudo2")

    # find unique interactions
    interactionsDetected = interactionData.Interaction.unique()

    cmd.group("Interactions", action="open")

    # neighbours - copy selection to new object
    cmd.create("neighbours", "neighbours")
    cmd.show_as("lines", "neighbours")
    cmd.show_as("spheres", "neighbours and metals")
    cmd.orient("neighbours")
    cmd.show_as("nb_spheres", "resn HOH and neighbours")

    # cmd.show("surface", "neighbours")
    # cmd.set("transparency", 0.9, "neighbours")



    ################## make visualization beautiful again! #####################

    # find number of poses
    noOfPoses = interactionData.Ligand_occurrence_in_sdf.max()


    increaseSphereFactor = 0.2 # increase the radius of spheres by adding this value
    multipleSphereFactor = 1.5 # multiple the radius of spheres by this value

    # assign parameters for non-hardcoded interactions
    for Interaction in interactionsDetected:
        # if this is NOT a hard-coded interaction, we will pick a new color and add it to the global dictionary
        # but which one to pick?
        if Interaction not in interactionColors:

            # assign colors
            interactionColors[Interaction] = interactionColorsOther[0]
            del interactionColorsOther[0] # remove this element from the main list.

            # assing other parameters
            interactionDashWidth[Interaction] = interactionDashWidthOther
            interactionDashGap[Interaction] = interactionDashGapOther

            # assign names
            interactionDesc[Interaction] = Interaction


    ### Draw interaction preferences ----- RECEPTOR -------
    if checkBox_ReceptorPreferences:

        form.label_15.setText("Calculating receptor prefs ...")


        interactionData['receptor_center'] = interactionData["Receptor_X"].astype(str) + '_' + interactionData["Receptor_Y"].astype(str) + '_' + interactionData["Receptor_Z"].astype(str)

        interactionDataGrouped = interactionData.groupby(['Interaction', 'receptor_center']).agg(['count'])['Ligand_name'].reset_index()
        maxCount = interactionDataGrouped['count'].max()
        interactionDataGrouped['percentage'] = interactionDataGrouped['count'] / maxCount

        points = {}
        for Interaction in interactionsDetected:

            kolor = cmd.get_color_tuple(cmd.get_color_index(interactionColors[Interaction]))
            points[Interaction] = [ COLOR, kolor[0],  kolor[1], kolor[2] ]

        rowNumber = 0
        for row in interactionDataGrouped.iterrows():

            rowNumber = i+1
            form.progressBar.setValue( int(rowNumber/interactionDataGroupedLen*100) )


            Interaction, receptor_center, count, percentage = row[1]
            #receptor_centerXYZ = receptor_center.split("_")
            receptor_centerXYZ = [float(x) for x in receptor_center.split("_") ]

            points[Interaction].extend([ SPHERE, receptor_centerXYZ[0], receptor_centerXYZ[1], receptor_centerXYZ[2], increaseSphereFactor + percentage*multipleSphereFactor])


        # cmd.load_cgo(point, "NuclAcid-%s" % (Interaction), state=0)
        for Interaction in points:
            cmd.load_cgo(points[Interaction], "ReceptorPreferences.Receptor--%s" % (Interaction), state=0)
            cmd.set('cgo_transparency',cgo_transparency,"ReceptorPreferences.Receptor--%s" % (Interaction), state=0)

        # cmd.group("%s--ReceptorPreferences" % (newObjectsPrefix), members="Receptor--*", action='auto')

    ### Draw interaction preferences ----- LIGANDS -------

    if checkBox_LigandPreferences:

        form.label_15.setText("Calculating ligand prefs ...")

        roundLigandPositionsDigits = 2 # group positions of ligand centers by rounding positions to this number of decimal digits;

        interactionData['ligand_center'] = round(interactionData["Ligand_X"], roundLigandPositionsDigits).astype(str) + '_' \
                + round(interactionData["Ligand_Y"], roundLigandPositionsDigits).astype(str) + '_' \
                + round(interactionData["Ligand_Z"], roundLigandPositionsDigits).astype(str)

        interactionDataGrouped = interactionData.groupby(['Interaction', 'ligand_center']).agg(['count'])['Ligand_name'].reset_index()
        maxCount = interactionDataGrouped['count'].max()
        interactionDataGrouped['percentage'] = interactionDataGrouped['count'] / maxCount

        points = {}
        for Interaction in interactionsDetected:
            kolor = cmd.get_color_tuple(cmd.get_color_index(interactionColors[Interaction]))
            points[Interaction] = [ COLOR, kolor[0],  kolor[1], kolor[2] ]

        rowNumber = 0
        for row in interactionDataGrouped.iterrows():

            rowNumber = i+1
            form.progressBar.setValue( int(rowNumber/interactionDataGroupedLen*100) )

            Interaction, ligand_center, count, percentage = row[1]
            #receptor_centerXYZ = receptor_center.split("_")
            ligand_centerXYZ = [float(x) for x in ligand_center.split("_") ]

            points[Interaction].extend([ SPHERE, ligand_centerXYZ[0], ligand_centerXYZ[1], ligand_centerXYZ[2], increaseSphereFactor + percentage*multipleSphereFactor])


        # cmd.load_cgo(point, "NuclAcid-%s" % (Interaction), state=0)
        for Interaction in points:
            cmd.load_cgo(points[Interaction], "LigandPreferences.Ligands--%s" % (Interaction), state=0)
            cmd.set('cgo_transparency',cgo_transparency,"LigandPreferences.Ligands--%s" % (Interaction), state=0)


        # cmd.group("%s--LigandPreferences" % (newObjectsPrefix), members="Ligands--*", action='auto')



    # --------- colors legend ---------
    print("---------- Colors legend: -----------")

    form.label_15.setText("Generating label object ...")

    for i, Interaction in enumerate(interactionColors):

        # legend as a next state

        pointName = "Legends.inter_%s" % (Interaction)
        distName = "Legends.inter__%s" % (Interaction)

        cmd.pseudoatom(pointName, pos=[Ligand_X+5, Ligand_Y+0+(1*i), Ligand_Z+0], state=noOfPoses+1)
        cmd.pseudoatom("skasuj", pos=[Ligand_X+0, Ligand_Y+0+(1*i), Ligand_Z+0], state=noOfPoses+1)
        cmd.distance( distName, "skasuj", pointName)
        cmd.delete("skasuj")
        cmd.label(pointName, '"%s" ' % (interactionDesc[Interaction]) )
        cmd.color(interactionColors[Interaction], distName)
        cmd.set('dash_gap', interactionDashGap[Interaction], distName, state=noOfPoses+1)
        cmd.set('dash_length', 0.3, distName, state=noOfPoses+1)
        cmd.set('dash_width', interactionDashWidth[Interaction], distName, state=noOfPoses+1)
        cmd.hide("wire", pointName)
        cmd.hide("labels", distName)
        cmd.set("label_position", [1.3,0,0], pointName, state=noOfPoses+1)

        # spheres
        kolor = cmd.get_color_tuple(cmd.get_color_index(interactionColors[Interaction]))
        point = [ COLOR, kolor[0],  kolor[1], kolor[2] ]
        point.extend([ SPHERE, Ligand_X+0, Ligand_Y+0+(1*i), Ligand_Z+0, 0.5])
        cmd.load_cgo(point, "Legends.prefs_%s" % (Interaction), state=noOfPoses+1)
        cmd.set('cgo_transparency',cgo_transparency,"Legends.prefs_%s" % (Interaction), state=noOfPoses+1)

        # coloring of all interactions detected
        if Interaction in interactionsDetected:
            cmd.set('dash_gap', interactionDashGap[Interaction], "Interactions.Inter--%s" % (Interaction), state=0)
            cmd.set('dash_length', 0.3, "Interactions.Inter--%s" % (Interaction), state=0)
            cmd.set('dash_width', interactionDashWidth[Interaction], "Interactions.Inter--%s" % (Interaction), state=0)
            cmd.color(interactionColors[Interaction], "Interactions.Inter--%s" % (Interaction))

        print("  %s (%s) is presented in %s" % (interactionDesc[Interaction], Interaction, interactionColors[Interaction]) )

    print("The color legend is displayed as the last state (go to the last state to see)")
    # cmd.group("%s--Legends" % (newObjectsPrefix), members="legend*", action='auto')


    # renaming objects if newObjectsPrefix is set

    if newObjectsPrefix != '':
        cmd.set_name("Interactions", "%s--Interactions" % (newObjectsPrefix) )
        cmd.set_name("ReceptorPreferences", "%s--ReceptorPreferences" % (newObjectsPrefix) )
        cmd.set_name("LigandPreferences", "%s--LigandPreferences" % (newObjectsPrefix) )
        cmd.set_name("Legends", "%s--Legends" % (newObjectsPrefix) )

        # and pack it into a group
        cmd.group("%s--fingernat" % (newObjectsPrefix),
                members="%s--Interactions %s--ReceptorPreferences %s--LigandPreferences %s--Legends" % (newObjectsPrefix,newObjectsPrefix,newObjectsPrefix,newObjectsPrefix),
                action='auto')

        cmd.group("%s--fingernat" % (newObjectsPrefix), action="open")


    # final orientation of the scene
    cmd.orient("neighbours")
    form.label_15.setText("Done!")
