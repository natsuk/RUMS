from Tkinter import *
import ttk
import types
import thread
#id_pass = tk.StringVar()
#id_pass.set("")

class UI():
    def final(self,event):
        print "final"
        #global root
        print self.entry1.get()
        self.root.destroy()
        #self.root.quit()

    def ui(self):
        print "in"
        self.root = Tk()
        self.root.title('Login Form')
        self.frame1 = ttk.Frame(self.root)
        self.label1 = ttk.Label(self.frame1, text = 'Input password')
        self.button1 = ttk.Button(self.frame1,text = 'OK')
        self.entry1 = ttk.Entry(self.frame1, width = 15, show = '*')
        self.frame1.grid(row = 0, column = 0, sticky = (N,E,S,W))
        self.label1.grid(row = 3, column = 2, sticky = E)
        self.button1.grid(row = 4, column = 2)
        self.button1.bind("<Button-1>",self.final)
        self.button1.bind("<Return>",self.final)
        self.entry1.grid(row = 2,column = 2)
        for child in self.frame1.winfo_children():
            child.grid_configure(padx = 5,pady = 5)
        self.root.mainloop()
        #print self.entry1.get()

    #def ui2(self):
        
#id_pass = entry1.get()
#print id_pass
#print type(id_pass)


if __name__=='__main__':
    t_ui=UI()
    t_ui.ui()
    t_ui.ui()
