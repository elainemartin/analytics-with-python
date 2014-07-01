import wx
import wx.lib.filebrowsebutton as filebrowse
import ast      #takes a string that looks like a list and turn it into a list
import gettext
import sys
import os.path
import Network as bn
import Node as nd
import Persistence 
import Inference           
      
class MainFrame(wx.Frame):
    """Main Application Frame"""
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        self.SetBackgroundColour("white")

        main_box = wx.BoxSizer(orient=wx.VERTICAL)
        panels_box = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.panel1 = wx.Panel(self, -1,style=wx.SUNKEN_BORDER)
        self.panel2 = wx.Panel(self, -1,style=wx.SUNKEN_BORDER)

        self.log = wx.TextCtrl(self, -1, size=(480,500),
                                   style = wx.TE_MULTILINE|wx.TE_READONLY|
                                   wx.HSCROLL)
        panels_box.Add(self.panel1, 1, wx.EXPAND)
        panels_box.Add(self.log, 1, wx.EXPAND)

        # Redirect stdout to capture all the print statements       
        redir=RedirectText(self.log)
        sys.stdout=redir
        print("Welcome Kingsley!!!")
 
        self.Bind(wx.EVT_CLOSE, self.CloseEventHandler)
        
        # Menu Bar
        self.frame_1_menubar = wx.MenuBar()
        self.File = wx.Menu()
        self.LoadNetwork = wx.MenuItem(self.File, 11, _("Load Network"), _("Load JSON Network File"), wx.ITEM_NORMAL)
        self.File.Append(self.LoadNetwork)
        self.SaveNetwork = wx.MenuItem(self.File, 12, _("Save Network"), _("Save Network to JSON File"), wx.ITEM_NORMAL)
        self.File.Append(self.SaveNetwork)
        self.Quit = wx.MenuItem(self.File, 13, _("Quit"), _("Quit App"), wx.ITEM_NORMAL)
        self.File.Append(self.Quit)
        self.frame_1_menubar.Append(self.File, _("File"))
        self.Network = wx.Menu()
        self.NewNetwork = wx.MenuItem(self.Network, 21, _("New Network"), _("Create a New Network"), wx.ITEM_NORMAL)
        self.Network.Append(self.NewNetwork)
        self.ViewNetwork = wx.MenuItem(self.Network, 22, _("View Network"), _("Visualize Network"), wx.ITEM_NORMAL)
        self.Network.Append(self.ViewNetwork)
        self.PrintNetwork = wx.MenuItem(self.Network, 23, _("Print Network"), _("Print Network"), wx.ITEM_NORMAL)
        self.Network.Append(self.PrintNetwork)
        self.DoInference = wx.MenuItem(self.Network, 24, _("Do Inference"), _("Do Inference on the Network"), wx.ITEM_NORMAL)
        self.Network.Append(self.DoInference)
        self.ClearAll = wx.MenuItem(self.Network, 25, _("Clear All"), _("Clear All Evidence And Belief On Network"), wx.ITEM_NORMAL)
        self.Network.Append(self.ClearAll)
        self.frame_1_menubar.Append(self.Network, _("Network"))
        self.Node = wx.Menu()
        self.CreateNode = wx.MenuItem(self.Node, 31, _("Create Node"), _("Create a New Node"), wx.ITEM_NORMAL)
        self.Node.Append(self.CreateNode)
        self.EditNode = wx.MenuItem(self.Node, 32, _("Edit Node"), _("Edit Existing Node"), wx.ITEM_NORMAL)
        self.Node.Append(self.EditNode)
        self.SetEvidence = wx.MenuItem(self.Node, 33, _("Set Evidence"), _("Set Evidence On Node"), wx.ITEM_NORMAL)
        self.Node.Append(self.SetEvidence)
        self.ClearEvidence = wx.MenuItem(self.Node, 34, _("Clear Evidence"), _("Clear Evidence On Chosen Node"), wx.ITEM_NORMAL)
        self.Node.Append(self.ClearEvidence)
        self.PrintEvidence = wx.MenuItem(self.Node, 35, _("Print Evidence"), _("Print Evidence for the Network"), wx.ITEM_NORMAL)
        self.Node.Append(self.PrintEvidence)
        self.SetBelief = wx.MenuItem(self.Node, 36, _("Set Belief"), _("Set Belief For a Specific Node"), wx.ITEM_NORMAL)
        self.Node.Append(self.SetBelief)
        self.ClearBelief = wx.MenuItem(self.Node, 37, _("Clear Belief"), _("Clear Current Belief"), wx.ITEM_NORMAL)
        self.Node.Append(self.ClearBelief)
        self.PrintBelief  = wx.MenuItem(self.Node, 38, _("Print Belief "), _("Print Belief for the Network"), wx.ITEM_NORMAL)
        self.Node.Append(self.PrintBelief )
        self.frame_1_menubar.Append(self.Node, _("Node"))
        self.Help = wx.Menu()
        self.About = wx.MenuItem(self.Help, 41, _("About"), _("Help? Ur a PhD student. c'mon really?"), wx.ITEM_NORMAL)
        self.Help.Append(self.About)
        self.frame_1_menubar.Append(self.Help, _("Help"))
        self.SetMenuBar(self.frame_1_menubar)
        
        self.Bind(wx.EVT_MENU, self.LoadNetworkEventHandler, self.LoadNetwork)
        self.Bind(wx.EVT_MENU, self.SaveNetworkEventHandler, self.SaveNetwork)
        self.Bind(wx.EVT_MENU, self.QuitEventHandler, self.Quit)
        self.Bind(wx.EVT_MENU, self.NewNetworkEventHandler, self.NewNetwork)
        self.Bind(wx.EVT_MENU, self.ViewNetworkEventHandler, self.ViewNetwork)
        self.Bind(wx.EVT_MENU, self.PrintNetworkEventHandler, self.PrintNetwork)
        self.Bind(wx.EVT_MENU, self.DoInferenceEventHandler, self.DoInference)
        self.Bind(wx.EVT_MENU, self.ClearAllEventHandler, self.ClearAll)
        self.Bind(wx.EVT_MENU, self.CreateNodeEventHandler, self.CreateNode)
        self.Bind(wx.EVT_MENU, self.EditNodeEventHandler, self.EditNode)
        self.Bind(wx.EVT_MENU, self.SetEvidenceEventHandler, self.SetEvidence)
        self.Bind(wx.EVT_MENU, self.ClearEvidenceEventHandler, self.ClearEvidence)
        self.Bind(wx.EVT_MENU, self.PrintEvidenceEventHandler, self.PrintEvidence)
        self.Bind(wx.EVT_MENU, self.SetBeliefEventHandler, self.SetBelief)
        self.Bind(wx.EVT_MENU, self.ClearBeliefEventHandler, self.ClearBelief)
        self.Bind(wx.EVT_MENU, self.PrintBeliefEventHandler, self.PrintBelief)
        self.Bind(wx.EVT_MENU, self.AboutEventHandler, self.About)
        # Menu Bar end
        
        # Status Bar
        self.frame_1_statusbar = self.CreateStatusBar(1, 0)
        # Status Bar end
        
        # Tool Bar
        self.frame_1_toolbar = wx.ToolBar(self, -1)
        self.SetToolBar(self.frame_1_toolbar)

        tb = wx.ToolBar(self, -1)
        self.ToolBar = tb
 
        tsize = (18,18)
        load_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, tsize)
        save_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE_AS, wx.ART_TOOLBAR, tsize)
        new_net_bmp =  wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, tsize)
        new_node_bmp =  wx.ArtProvider.GetBitmap(wx.ART_ADD_BOOKMARK, wx.ART_TOOLBAR, tsize)
        edit_node_bmp =  wx.ArtProvider.GetBitmap(wx.ART_LIST_VIEW, wx.ART_TOOLBAR, tsize)
        belief_bmp= wx.ArtProvider.GetBitmap(wx.ART_QUESTION, wx.ART_TOOLBAR, tsize)
        evidence_bmp= wx.ArtProvider.GetBitmap(wx.ART_TICK_MARK, wx.ART_TOOLBAR, tsize)
        clear_bmp= wx.ArtProvider.GetBitmap(wx.ART_CROSS_MARK, wx.ART_TOOLBAR, tsize)
        inference_bmp= wx.ArtProvider.GetBitmap(wx.ART_FIND_AND_REPLACE, wx.ART_TOOLBAR, tsize)
        #help_bmp= wx.ArtProvider.GetBitmap(wx.ART_HELP, wx.ART_TOOLBAR, tsize)
        #info_bmp= wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_TOOLBAR, tsize)
        about_bmp= wx.ArtProvider.GetBitmap(wx.ART_TIP, wx.ART_TOOLBAR, tsize)
        quit_bmp= wx.ArtProvider.GetBitmap(wx.ART_QUIT, wx.ART_TOOLBAR, tsize)
        tb.SetToolBitmapSize(tsize)

        tb.AddTool(10, "Load", load_bmp, shortHelp="Load an existing network")
        tb.AddTool(20, "Save", save_bmp, shortHelp="Save the current network")
        tb.AddSeparator()
        tb.AddTool(30, "NewNet", new_net_bmp, shortHelp="Create a new network")
        tb.AddTool(40, "NewNode", new_node_bmp, shortHelp="Create a new node")
        tb.AddTool(50, "Edit", edit_node_bmp, shortHelp="Edit a node")
        tb.AddSeparator() 
        tb.AddTool(60, "SetB", belief_bmp, shortHelp="Set belief")     
        tb.AddTool(70, "SetE", evidence_bmp, shortHelp="Set evidence")     
        tb.AddTool(80, "Clear", clear_bmp, shortHelp="Clear all belief and evidence")     
        tb.AddTool(90, "Do", inference_bmp, shortHelp="Do inference")  
        tb.AddSeparator()                    
        #tb.AddTool(100, "Help", help_bmp, shortHelp="Obtain help")
        #tb.AddTool(110, "Info", info_bmp, shortHelp="Obtain information")
        tb.AddTool(120, "About", about_bmp, shortHelp="About this application")  
        tb.AddTool(130, "Quit", quit_bmp, shortHelp="Quit this application")

        self.Bind(wx.EVT_TOOL, self.LoadNetworkEventHandler, id=10)
        self.Bind(wx.EVT_TOOL, self.SaveNetworkEventHandler, id=20)
        self.Bind(wx.EVT_TOOL, self.NewNetworkEventHandler, id=30)
        self.Bind(wx.EVT_TOOL, self.CreateNodeEventHandler, id=40)
        self.Bind(wx.EVT_TOOL, self.EditNodeEventHandler, id=50)
        self.Bind(wx.EVT_TOOL, self.SetBeliefEventHandler, id=60)
        self.Bind(wx.EVT_TOOL, self.SetEvidenceEventHandler, id=70)
        self.Bind(wx.EVT_TOOL, self.ClearAllEventHandler, id=80)
        self.Bind(wx.EVT_TOOL, self.DoInferenceEventHandler, id=90)
        #self.Bind(wx.EVT_TOOL, self.HelpEventHandler, id=100)
        #self.Bind(wx.EVT_TOOL, self.InfoEventHandler, id=110)
        self.Bind(wx.EVT_TOOL, self.AboutEventHandler, id=120)
        self.Bind(wx.EVT_TOOL, self.QuitEventHandler, id=130)
        #self.Bind(wx.EVT_TOOL, self.ViewNetworkEventHandler, self.ViewNetwork)
        #self.Bind(wx.EVT_TOOL, self.ClearEvidenceEventHandler, self.ClearEvidence)
        #self.Bind(wx.EVT_TOOL, self.ClearBeliefEventHandler, id=80)
                
        tb.Realize()
        # Tool Bar end
        
        main_box.Add(tb, 0, wx.EXPAND)
        main_box.Add(panels_box, 1, wx.EXPAND)
        self.SetAutoLayout(True)
        self.SetSizer(main_box)
        self.Layout() 

        # Initialize a network
        self.BayesNet = bn.Network()
        self.displayNetwork()
              
    def displayNetwork(self):
        if os.path.isfile('./myNetFig.png'):
            img = wx.Image('./myNetFig.png', wx.BITMAP_TYPE_ANY) 
            img = img.Scale(480, 430, wx.IMAGE_QUALITY_HIGH)
        else:
            if os.path.isfile('./myDefaultNetFig.png'):
                img = wx.Image('./myDefaultNetFig.png', wx.BITMAP_TYPE_ANY) 
                img = img.Scale(480, 430, wx.IMAGE_QUALITY_HIGH)
            else: 
                img = wx.EmptyImage(480,430)
        self.imageCtrl = wx.StaticBitmap(self.panel1, wx.ID_ANY, 
                                         wx.BitmapFromImage(img))
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.mainSizer.Add(self.imageCtrl, 0, wx.EXPAND)    
        self.panel1.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self.panel1)
        self.panel1.Layout()   
         
    def LoadNetworkEventHandler(self, event):
        self.frame2 = wx.Frame(None, title = "Load Network from JSON File")

        self.frame2.fbb = filebrowse.FileBrowseButton(
            self.frame2, -1, size=(450, -1), changeCallback = self.fbbCallback2
            )
        self.frame2.cancelButton = wx.Button(self.frame2, -1, label = "Cancel")
        self.frame2.okButton = wx.Button(self.frame2, -1, label = "OK" )  
 
        self.frame2.hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.frame2.hbox.AddSpacer(200)
        self.frame2.hbox.Add(self.frame2.cancelButton, flag =  wx.ALL, border = 5)
        self.frame2.hbox.Add(self.frame2.okButton, flag =  wx.ALL, border = 5)                 
        
        self.frame2.vbox = wx.BoxSizer(wx.VERTICAL) 
        self.frame2.vbox.Add(self.frame2.fbb, flag =  wx.ALL, border = 5)
        self.frame2.vbox.Add(self.frame2.hbox, flag =  wx.ALL, border = 5)

        self.frame2.cancelButton.Bind(wx.EVT_BUTTON, self.LoadNetworkCancelEventHandler)
        self.frame2.okButton.Bind(wx.EVT_BUTTON, self.LoadNetworkOKEventHandler)

        self.frame2.SetSizerAndFit(self.frame2.vbox)  
        self.frame2.Centre()
        self.frame2.Show()
        
    def fbbCallback2(self, event):
        pass

    def LoadNetworkOKEventHandler(self,event):
        self.BayesNet = bn.Network()
        js2 = Persistence.readFile(self.frame2.fbb.GetValue())
        self.BayesNet.from_JSON(js2)
        self.frame2.Destroy()
        self.BayesNet.drawNetwork()
        self.displayNetwork()
        print('Network loaded from: ',self.frame2.fbb.GetValue())

    def LoadNetworkCancelEventHandler(self, event):
        self.frame2.Destroy()

    def SaveNetworkEventHandler(self, event): 
        self.frame3 = wx.Frame(None, title = "Save Network to JSON File")

        self.frame3.fbb = filebrowse.FileBrowseButton(
            self.frame3, -1, size=(450, -1), changeCallback = self.fbbCallback3
            )
        self.frame3.cancelButton = wx.Button(self.frame3, -1, label = "Cancel")
        self.frame3.okButton = wx.Button(self.frame3, -1, label = "OK" )  
 
        self.frame3.hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.frame3.hbox.AddSpacer(200)
        self.frame3.hbox.Add(self.frame3.cancelButton, flag =  wx.ALL, border = 5)
        self.frame3.hbox.Add(self.frame3.okButton, flag =  wx.ALL, border = 5)                 
        
        self.frame3.vbox = wx.BoxSizer(wx.VERTICAL) 
        self.frame3.vbox.Add(self.frame3.fbb, flag =  wx.ALL, border = 5)
        self.frame3.vbox.Add(self.frame3.hbox, flag =  wx.ALL, border = 5)

        self.frame3.cancelButton.Bind(wx.EVT_BUTTON, self.SaveNetworkCancelEventHandler)
        self.frame3.okButton.Bind(wx.EVT_BUTTON, self.SaveNetworkOKEventHandler)

        self.frame3.SetSizerAndFit(self.frame3.vbox)  
        self.frame3.Centre()
        self.frame3.Show()
        
        self.frame3.Centre()
        self.frame3.Show()
        
    def fbbCallback3(self, event):
        pass

    def SaveNetworkOKEventHandler(self,event):
        Persistence.saveFile(self.frame3.fbb.GetValue(), self.BayesNet.to_JSON())
        print('Network saved to: ',self.frame3.fbb.GetValue())
        self.frame3.Destroy()

    def SaveNetworkCancelEventHandler(self, event):
        self.frame3.Destroy()
 
    def CloseEventHandler(self, event):
        if os.path.isfile('./myNetFig.png'):
            os.remove('./myNetFig.png')
        self.Destroy()
        
    def QuitEventHandler(self, event):
        if os.path.isfile('./myNetFig.png'):
            os.remove('./myNetFig.png')
        self.Close(True)

    def NewNetworkEventHandler(self, event):
        dlg = wx.TextEntryDialog(self, 'Please enter network name:',"New Network","", style=wx.OK)
        dlg.ShowModal()
        name = dlg.GetValue()
        dlg.Destroy()
        self.BayesNet = bn.Network(name)
        self.BayesNet.drawNetwork()
        self.displayNetwork()
        print('Network ' + name + ' created')

    def ViewNetworkEventHandler(self, event):
        self.BayesNet.drawNetwork()
        self.displayNetwork()

    def PrintNetworkEventHandler(self, event):
        self.BayesNet.printNetwork()

    def DoInferenceEventHandler(self, event):
        Inference.doInference(self.BayesNet)

    def ClearAllEventHandler(self, event): 
        for node in self.BayesNet.nodes:
            node.clearEvidence()
            node.clearBelief()
        print('All belief and evidence cleared for the network')

    def CreateNodeEventHandler(self, event):  
        # Set the name for a node
        dlg = wx.TextEntryDialog(self, 'Node Name:','Create Node','' ,style=wx.OK|wx.CANCEL)
        if dlg.ShowModal() == wx.ID_OK:
            nodeName = dlg.GetValue()
            dlg2 = wx.TextEntryDialog(self, 'CPT Name:','Create Node','' ,style=wx.OK|wx.CANCEL)
            if dlg2.ShowModal() == wx.ID_OK:
                cptName = dlg2.GetValue()
            # Set the CPT for the given node
                dlg3 = wx.TextEntryDialog(self, 'Node CPT:','Create Node','',style=wx.OK|wx.CANCEL)
                if dlg3.ShowModal() == wx.ID_OK:
                    nodeCPT = dlg3.GetValue()
                    nodeCPT = ast.literal_eval(nodeCPT) 
                    # Create the new node and add it to the Bayesian Network
                    newNode = nd.Node(nodeName)
                    newNode.setCPT(cptName, nodeCPT)
                    self.BayesNet.addNode(newNode)
        dlg.Destroy()
        self.BayesNet.drawNetwork()
        self.displayNetwork()

    def EditNodeEventHandler(self, event):  
        nodeList = self.BayesNet.getNetwork()
        dlg = wx.SingleChoiceDialog(self, 'Node Name:', 'Edit Node',nodeList, wx.CHOICEDLG_STYLE)

        if dlg.ShowModal() == wx.ID_OK:    
            selectedNode = dlg.GetStringSelection()
            dlg2 = wx.TextEntryDialog(self, 'New Node Name:','Edit Node','',style=wx.OK|wx.CANCEL)
            if dlg2.ShowModal() == wx.ID_OK:
                newName = dlg2.GetValue()
                self.BayesNet.getNode(selectedNode).setName(newName)
                dlg2.Destroy()
                dlg3 = wx.TextEntryDialog(self, 'CPT Name:','Edit Node','' ,style=wx.OK|wx.CANCEL)
                if dlg3.ShowModal() == wx.ID_OK:
                    cptName = dlg3.GetValue()
                    dlg3.Destroy()
                    # Set the CPT for the given node
                    dlg4 = wx.TextEntryDialog(self, 'Node CPT:','Edit Node','',style=wx.OK|wx.CANCEL)
                    if dlg4.ShowModal() == wx.ID_OK:
                        nodeCPT = dlg4.GetValue()
                        nodeCPT = ast.literal_eval(nodeCPT) 
                        self.BayesNet.getNode(newName).setCPT(cptName,nodeCPT)
                        dlg4.Destroy()
        dlg.Destroy()
        self.BayesNet.drawNetwork()
        self.displayNetwork()

    def SetEvidenceEventHandler(self, event): 
        nodeList = self.BayesNet.getNetwork()
        dlg = wx.SingleChoiceDialog(self, 'Select a Dimension:', 'Set Evidence',nodeList, wx.CHOICEDLG_STYLE)
        if dlg.ShowModal() == wx.ID_OK:    
            dim = dlg.GetStringSelection()
            dlg2 = wx.TextEntryDialog(self, 'How many states in ' + dim + ' are there?:','Set Evidence','',style=wx.OK|wx.CANCEL)
            if dlg2.ShowModal() == wx.ID_OK:
                table = int(dlg2.GetValue())
                dlg2.Destroy()
                dlg3 = wx.TextEntryDialog(self, 'Which state in ' + dim + ' you setting?','Set Evidence','' ,style=wx.OK|wx.CANCEL)
                if dlg3.ShowModal() == wx.ID_OK:
                    index = int(dlg3.GetValue())-1
                    dlg3.Destroy()
                self.BayesNet.getNode(dim).setEvidence(dim,table,index)
                self.BayesNet.printEvidence()
        dlg.Destroy()

    def ClearEvidenceEventHandler(self, event):  
        nodeEvidenceList = self.BayesNet.getEvidence()
        dlg = wx.SingleChoiceDialog(self, 'Clear Evidence on Which Node:', 'Clear Evidence',nodeEvidenceList, wx.CHOICEDLG_STYLE)
        if dlg.ShowModal() == wx.ID_OK:    
            selectedNode = dlg.GetStringSelection()
            self.BayesNet.getNode(selectedNode).clearEvidence()
            dlg2 = wx.MessageDialog(self,
                           message='Evidence on node %s cleared!'%selectedNode,
                           caption='',
                           style=wx.OK|wx.ICON_INFORMATION
                           )
            dlg2.ShowModal()
            self.BayesNet.printEvidence()
        dlg.Destroy()

    def PrintEvidenceEventHandler(self, event):
        self.BayesNet.printEvidence()

    def SetBeliefEventHandler(self, event):
        nodeList = self.BayesNet.getNetwork()
        dlg = wx.SingleChoiceDialog(self, 'Set belief on node:', 'Set Belief',nodeList, wx.CHOICEDLG_STYLE)
        if dlg.ShowModal() == wx.ID_OK:    
            selectedNode = dlg.GetStringSelection()
            self.BayesNet.getNode(selectedNode).setBelief()
            self.BayesNet.printBelief()
        dlg.Destroy()
        

    def ClearBeliefEventHandler(self, event):
        nodeName = None
        for node in self.BayesNet.nodes:
            if node.getBelief():
                nodeName = node.name
        if nodeName is not None:
            dlg = wx.MessageDialog(self, 'Clear belief on node '+nodeName+'?', 'Clear Belief',style=wx.OK|wx.CANCEL)
            if dlg.ShowModal() == wx.ID_OK:    
                self.BayesNet.getNode(nodeName).clearBelief()
                self.BayesNet.printBelief()
            dlg.Destroy()
        else:
            dlg = wx.MessageDialog(self, 'Belief has not yet been set. Would you like to set belief now?', 'Error',style=wx.OK|wx.CANCEL)
            if dlg.ShowModal() == wx.ID_OK:    
                self.SetBeliefEventHandler(self.SetBelief)
                self.BayesNet.printBelief()
            dlg.Destroy()
            
    def PrintBeliefEventHandler(self, event):
        self.BayesNet.printBelief()
        
    def AboutEventHandler(self, event):  
        dlg = wx.MessageDialog( self, "A Bayesian Network GUI", "About BayesNetX Application", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
    
# end of class MyFrame 
class RedirectText:
    def __init__(self,aWxTextCtrl):
        self.out=aWxTextCtrl

    def write(self,string):
        self.out.WriteText(string)

if __name__ == "__main__":
    
    gettext.install("app")         # replace with the appropriate catalog name
    app = wx.App(redirect=False)        
    frame_1 = MainFrame(None, -1, "Bayes Net Application", size=(960,500))
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()








