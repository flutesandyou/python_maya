import maya.cmds as cmds
import maya.mel as mel
import os

def openDialog(path=True):
    if path == True:
        openDialog.path = "".join(openDialog.path)
        return openDialog.path
    elif path == False:
        openDialog.path = cmds.fileDialog2(fm=3)

def buttonCommand(*args):
    openDialog(path=False)
    list1 = openDialog(path=True)
    cmds.textField(buildUI.textFieldObj, edit=1, tx=list1)

def buttonCommand2(*args):
    openDialog(path=False)
    list2 = openDialog(path=True)
    cmds.textField(buildUI.textFieldObj2, edit=1, tx=list2)

def checkBoxState(*args):
    checkBoxState.value = 0
    if cmds.checkBox(buildUI.fbxCheckbox, q=1, v=1) == True and cmds.checkBox(buildUI.daeCheckbox, q=1, v=1) == False:
        print 'FBX'
        checkBoxState.value = 1
        print checkBoxState.value
    elif cmds.checkBox(buildUI.daeCheckbox, q=1, v=1) == True and cmds.checkBox(buildUI.fbxCheckbox, q=1, v=1) == False:
        print 'DAE'
        checkBoxState.value = 2
        print checkBoxState.value
    elif cmds.checkBox(buildUI.fbxCheckbox, q=1, v=1) == True and cmds.checkBox(buildUI.daeCheckbox, q=1, v=1) == True:
        print 'FBX, DAE'
        checkBoxState.value = 3
        print checkBoxState.value
    else:
        print 'nothing'
        checkBoxState.value = 0
        print checkBoxState.value

def buildUI():
    winName = 'exporter'
    winWidth = 200 # set a target width and reference this when you specify width
    if cmds.window(winName, exists=True):
          cmds.deleteUI(winName)
    window = cmds.window(winName, width=winWidth, title='Batch Exporter')
    mainCL = cmds.columnLayout(adj=1, rowSpacing=3,)
    tmpRowWidth = [winWidth*0.3, winWidth*0.7]

    cmds.rowLayout(numberOfColumns=3, columnWidth2=tmpRowWidth, ct3=('both','both','both'), cl3=('both','both','both'), co3=(5,15,5))
    cmds.text('File Format:')
    buildUI.fbxCheckbox = cmds.checkBox( label='fbx', onc=checkBoxState, ofc=checkBoxState) # then take states of this cbx
    buildUI.daeCheckbox = cmds.checkBox( label='dae', onc=checkBoxState, ofc=checkBoxState) # then take states of this cbx
    cmds.setParent('..')

    cmds.rowLayout(numberOfColumns=3, columnWidth2=tmpRowWidth, adj=2, ct3=('both','both','both'), co3=(5,5,5))
    cmds.text('Source Directory:')
    list1 = ''
    if list1 != '':
        buildUI.textFieldObj = cmds.textField(text=list1, w=250)
    else:
        buildUI.textFieldObj = cmds.textField(text='', w=250)
    buttonObj = cmds.button(label='Set', c=buttonCommand)
    cmds.setParent('..')

    cmds.rowLayout(numberOfColumns=3, columnWidth2=tmpRowWidth, adj=2, ct3=('both','both','both'), co3=(5,5,5))
    cmds.text('Save Directory:')
    list2 = ''
    if list2 != '':
        buildUI.textFieldObj2 = cmds.textField(text=list2, w=250)
    else:
        buildUI.textFieldObj2 = cmds.textField(text='', w=250)
    buttonObj = cmds.button(label='Set', c=buttonCommand2)
    cmds.setParent('..')

    buttonObj3 = cmds.button(label='Run', c=batchExport)

    cmds.showWindow( winName )

def batchExport(*args):
    #dae fbx exporter settings:
    mel.eval("FBXResetExport")
    mel.eval("FBXExportColladaFrameRate 25")
    mel.eval("FBXExportColladaSingleMatrix false")
    mel.eval("FBXExportColladaTriangulate false")
    mel.eval("FBXExportCameras -v false")
    mel.eval("FBXExportLights -v false")

    # get source and save directories from UI:
    SourceDirectory = ''
    SaveDirectory = ''

    if cmds.textField(buildUI.textFieldObj, q=1, tx=1) == '':
        cmds.warning('no Source Directory selected')
    else:
        SourceDirectory = (''.join(cmds.textField(buildUI.textFieldObj, q=1, tx=1)) + '/')

    if cmds.textField(buildUI.textFieldObj2, q=1, tx=1) == '':
        cmds.warning('no Save Directory selected')
    else:
        SaveDirectory = (''.join(cmds.textField(buildUI.textFieldObj2, q=1, tx=1)) + '/')

    print(SourceDirectory)

    filesList = []
    # get list of files in source directory:
    dir = SourceDirectory
    if checkBoxState.value == 1:
        for root, dirs, files in os.walk(SourceDirectory):
            for file in files:
                if file.endswith(".fbx"):
                    filesList.append(os.path.relpath(root, start=dir) + "\\" + file)
    elif checkBoxState.value == 2:
        for root, dirs, files in os.walk(SourceDirectory):
            for file in files:
                if file.endswith(".dae"):
                    filesList.append(os.path.relpath(root, start=dir) + "\\" + file)
    elif checkBoxState.value == 3:
        for root, dirs, files in os.walk(SourceDirectory):
            for file in files:
                if file.endswith(".dae") or file.endswith(".fbx"):
                    filesList.append(os.path.relpath(root, start=dir) + "\\" + file)  
    else:
        cmds.warning('no file format selected')
    print(filesList)
    rootObj = '*root*'

    if filesList == None:
        cmds.warning('no files found in Source Directory')
    else:
        for i in filesList:
            cmds.file(f=1, new=1)

            curFile = SourceDirectory + i
            curFile = os.path.normpath(curFile)
            curFile = curFile.replace(os.sep, '/')
            print(curFile)
            cmds.file(curFile, i=1, ignoreVersion=1, renameAll=1, mergeNamespacesOnClash=0, namespace='add', options='fbx', preserveReferences=1, ifr=1, itr="override")

            print('imported: ' + curFile)

            #function call
            if cmds.objExists(rootObj):
                #change framerate
                cmds.currentUnit(t='ntsc')

                procedure0()
                cmds.select(rootObj, r=1)
                fileOut = (SaveDirectory + i)
                fileOut = os.path.normpath(fileOut)
                print('file to be saved: ' + fileOut)

                if 'fbx' not in i:
                    fileType = 'DAE_FBX export'
                else:
                    fileType = 'FBX export'

                path = i.rsplit('\\',1)[0]
                path = SaveDirectory + path
                print(path)
                if os.path.isdir(path):
                    pass
                else:
                    os.makedirs(path)

                cmds.file(fileOut, force=1, options='v=0', type=fileType, pr=1, es=1)
                cmds.delete(rootObj)
                cmds.warning(fileOut + ' SAVED' + '\n' + '\n')
            else:
                pass

buildUI()
