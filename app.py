import csv
import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, LEFT, RIDGE, simpledialog
from tkinter.ttk import *
from tkinter.colorchooser import *
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

password = ''


def getpwd():
    tempRoot = tk.Tk()
    tempRoot.geometry('300x150')
    tempRoot.title('')
    pwdbox = Entry(tempRoot, show='*')

    def onpwdentry(evt):
        global password
        password = pwdbox.get()
        tempRoot.destroy()

    def onokclick():
        global password
        password = pwdbox.get()
        tempRoot.destroy()

    Label(tempRoot, text='Enter your Password').pack(side='top', padx=10, pady=10)

    pwdbox.pack(side='top')
    pwdbox.bind('<Return>', onpwdentry)
    Button(tempRoot, command=onokclick, text='OK').pack(side='top', padx=10, pady=10)

    tempRoot.mainloop()
    return password


# Change the default Operating System
def change_default_os():
    desOS = osCombo.get()
    num = 0
    if desOS == 'Ubuntu':
        num = 1
    elif desOS == 'Windows':
        num = 4
    print(num)
    temp = 's/GRUB_DEFAULT=.*/GRUB_DEFAULT=' + str(num) + '/'
    cmd = 'sed - i ' + temp + ' /etc/default/grub'
    p = os.system('echo %s|sudo -S %s' % (password, cmd))
    print(p)
    command2 = 'sudo update-grub'
    p = os.system('echo %s|sudo -S %s' % (password, command2))
    print(p)
    # Display a message
    messagebox.showinfo('Success', 'Default Operating System Changed')


# Change Splash Screen color
def change_splash_color():
    color = askcolor(color="#dd4814")
    list_ = list(color[0])
    colorList = []
    for a in list_:
        a = float(a) / 255
        colorList.append(round(a, 2))

    color_tuple = tuple(colorList)
    new_color = str(color_tuple)
    print(new_color)
    cmd = "echo \"" + password + "\" | sudo -S sed -i \"s/^Window.SetBackgroundTopColor .*$/Window.SetBackgroundTopColor " + new_color + ";     # Nice colour on top of the screen fading to/g\" \"/usr/share/plymouth/themes/ubuntu-logo/ubuntu-logo.script\""
    cmd2 = "echo \"" + password + "\" | sudo -S sed -i \"s/^Window.SetBackgroundBottomColor .*$/Window.SetBackgroundBottomColor " + new_color + ";     # an equally nice colour on the bottom/g\" \"/usr/share/plymouth/themes/ubuntu-logo/ubuntu-logo.script\""
    print(cmd)
    subprocess.call(cmd, shell=True)
    subprocess.call(cmd2, shell=True)
    subprocess.call(['sudo', 'update-initramfs', '-u'])
    messagebox.showinfo("Splash Screen Color", "Successfully changed")


# Change the time-out period shown in GRUB
def set_grub_timeout():
    timeout = grubTimeOutSpin.get()
    temp = 's/GRUB_TIMEOUT=.*/GRUB_TIMEOUT=' + str(timeout) + '/'
    command1 = 'sudo sed -i ' + temp + ' /etc/default/grub'
    p = os.system('echo %s|sudo -S %s' % (password, command1))
    print(p)
    command2 = 'sudo update-grub'
    p = os.system('echo %s|sudo -S %s' % (password, command2))
    print(p)
    print('grub timeout changed')
    # Display a message
    messagebox.showinfo('Success', 'Grub timeout changed')


# Change splash screen logo
def change_splash_logo():
    file_path = filedialog.askopenfilename(initialdir="/home", title="Select file",
                                           filetypes=(("jpeg files", "*.jpg"), ("png files", "*.png")))

    image_name = os.path.basename(file_path)
    print(file_path)

    if file_path != '':
        cmd = "sudo -S cp " + file_path + " /usr/share/plymouth/themes/ubuntu-logo"
        cmd2 = "sudo -S sed -i \'s/logo_filename = .*\"/logo_filename = \"" + image_name + "\"/\' /usr/share/plymouth/themes/ubuntu-logo/ubuntu-logo.script"
        print(cmd2)
        p = os.system('echo %s|sudo -S %s' % (password, cmd))
        print(p)
        p = os.system('echo %s|sudo -S %s' % (password, cmd2))
        print(p)
        subprocess.call(['sudo', 'update-initramfs', '-u'])
        messagebox.showinfo("Splash Screen Logo", "Successfully changed")

    else:
        messagebox.showwarning("WARNING", "Image not selected")


# Scheduling shutdown
def schedule_shutdown():
    tempRoot = tk.Tk()
    tempRoot.geometry('300x100')
    tempRoot.title('Schedule Shutdown')
    time = Entry(tempRoot)

    def onokclick():
        minutes = int(time.get())
        if minutes < 0:
            messagebox.showinfo('Shutdown Scheduling Failed', 'Invalid time!')
            time.delete(0, 'end')
        else:
            print('Scheduling shutdown')
            # Schedule shutdown
            cmd = 'sudo shutdown -h ' + str(minutes)
            p = os.system('echo %s|sudo -S %s' % (password, cmd))
            print('shutdown scheduled')
            print(p)
            tempRoot.destroy()

    Label(tempRoot, text='Enter time to shutdown the system(minutes)').pack(side='top', padx=10, pady=10)

    time.pack(side='top')
    Button(tempRoot, command=onokclick, text='Schedule').pack(side='top', padx=10, pady=10)

    tempRoot.mainloop()


# Scheduling restart
def schedule_restart():
    tempRoot = tk.Tk()
    tempRoot.geometry('300x100')
    tempRoot.title('Schedule Reboot')
    time = Entry(tempRoot)

    def onokclick():
        minutes = int(time.get())
        if minutes < 0:
            messagebox.showinfo('Reboot Scheduling Failed', 'Invalid time!')
            time.delete(0, 'end')
        else:
            print('Scheduling reboot')
            # Schedule reboot
            cmd = 'sudo shutdown -r ' + str(minutes)
            p = os.system('echo %s|sudo -S %s' % (password, cmd))
            print('reboot scheduled')
            print(p)
            tempRoot.destroy()

    Label(tempRoot, text='Enter time to reboot the system(minutes)').pack(side='top', padx=10, pady=10)

    time.pack(side='top')
    Button(tempRoot, command=onokclick, text='Schedule').pack(side='top', padx=10, pady=10)

    tempRoot.mainloop()


# Update memory usage graph
def update_memory_usage():
    command = "ps aux | awk 'NR>2{arr[$1]+=$6}END{for(i in arr) print i,arr[i]/1024}' > memory_usage.txt"
    p = os.system(command)
    x = []
    y = []
    with open('memory_usage.txt', 'r') as csv_file:
        plots = csv.reader(csv_file, delimiter=' ')
        for row in plots:
            x.append(row[0])
            y.append(float(row[1]))

    # print(x, y)
    plt.pie(y, labels=x, shadow=True)
    plt.show()


# Update memory usage graph
def update_cpu_usage():
    command = """ps aux | awk 'NR>2{arr[$1]+=$3}END{for(i in arr) print i,arr[i] " % "}' > cpu_usage.txt"""
    p = os.system(command)
    x = []
    y = []
    with open('cpu_usage.txt', 'r') as csv_file:
        plots = csv.reader(csv_file, delimiter=' ')
        for row in plots:
            x.append(row[0])
            y.append(float(row[1]))

    # print(x, y)
    plt.pie(y, labels=x, shadow=True)
    plt.show()


# Add user with given username and password
def add_user():
    newUserName = userName.get()
    newUserPassword = passwd.get()
    newUserConfPassword = confPasswd.get()
    usershell = new_shell.get()

    if len(newUserName) < 1:
        messagebox.showinfo('Can\'t create user', 'No Username specified')
        userName.delete(0, 'end')
        passwd.delete(0, 'end')
        confPasswd.delete(0, 'end')
    elif newUserPassword != newUserConfPassword:
        messagebox.showinfo('Can\'t create user', 'Passwords does\'nt match')
        confPasswd.delete(0, 'end')
    else:
        command = 'sudo useradd -m ' + newUserName + " -s " + usershell
        command2 = "echo \"" + newUserName + ":" + newUserPassword + "\" | sudo chpasswd -c SHA512"
        print(newUserPassword)
        p = os.system('echo %s|sudo -S %s' % (password, command))
        print(p)
        p = os.system('echo %s|sudo -S %s' % (password, command2))
        print(p)
        messagebox.showinfo('Success', 'User Added Successfully')


# Add users batch mode
def add_user_batch():
    csv_filename = filedialog.askopenfilename(initialdir="/home", title="Select CSV",
                                              filetypes=(("CSV files", "*.csv"), ("all files", "*.*")))
    print(csv_filename)
    data = pd.read_csv(csv_filename)
    df = pd.DataFrame(data)

    matrix = []
    usernames = []
    uids = []
    passwords = []
    shells = []
    print(df)
    for row in df.iterrows():
        matrix.append(row)

    range_lenth = len(matrix)

    for i in range(0, range_lenth):
        usernames.append(matrix[i][1][0])
        uids.append(str(matrix[i][1][1]))
        # encrypting password
        passwords.append(str(matrix[i][1][2]))
        shells.append(matrix[i][1][3])

    for i in range(0, range_lenth):
        cmd1 = "echo \"" + password + "\" | sudo -S groupadd -g \"" + uids[i] + "\" \"" + usernames[i] + "\""
        print(cmd1)
        cmd2 = "sudo useradd -m \"" + usernames[i] + "\" -u \"" + uids[i] + "\" -g \"" + uids[i] + "\" -s \"" + shells[
            i] + "\""
        cmd3 = "echo \"" + usernames[i] + ":" + passwords[i] + "\" | sudo chpasswd -c SHA512"
        print(cmd2)
        print(cmd3)
        subprocess.call(cmd1, shell=True)
        subprocess.call(cmd2, shell=True)
        subprocess.call(cmd3, shell=True)
    messagebox.showinfo("Add Users", "Successfully Added")


def update_cpu_usage():
    cwd = os.getcwd()
    subprocess.call(cwd + '/getcpu.sh')

    arr = []

    f = open("newcpu.txt", "r")
    for ele in f:
        if ele != "\n":
            arr.append(ele.rstrip())
        else:
            arr.append(0)
    f.close()

    print(arr)

    labels = []
    values = []
    explode = []
    for i in range(0, len(arr)):
        if i % 2 == 0:
            labels.append(arr[i])
        else:
            values.append(float(arr[i]))
    labels.append("idle")
    values.append(100 - sum(values))

    for i in range(0, len(labels)):
        explode.append(0.05)

    actualFigure = plt.figure(figsize=(5, 5))

    pie = plt.pie(values, labels=labels, explode=explode, shadow=True, autopct='%1.1f%%')
    canvas = FigureCanvasTkAgg(actualFigure, master=tab3)
    canvas.get_tk_widget().place(x=45, y=230, width=250, height=250)
    canvas.show()


def update_memory_usage():
    cwd = os.getcwd()
    subprocess.call(cwd + '/getmem.sh')

    arr = []

    f = open("newmem.txt", "r")
    for ele in f:
        if ele != "\n":
            arr.append(ele.rstrip())
        else:
            arr.append(0)
    f.close()

    print(arr)

    labels = []
    values = []
    explode = []
    for i in range(0, len(arr)):
        if i % 2 == 0:
            labels.append(arr[i])
        else:
            values.append(float(arr[i]))
    labels.append("idle")
    values.append(100 - sum(values))

    for i in range(0, len(labels)):
        explode.append(0.05)

    actualFigure = plt.figure(figsize=(8, 8))

    pie = plt.pie(values, labels=labels, explode=explode, shadow=True, autopct='%1.1f%%')
    canvas = FigureCanvasTkAgg(actualFigure, master=tab3)
    canvas.get_tk_widget().place(x=400, y=230, width=250, height=250)
    canvas.show()


# Get the user password
password = getpwd()
print(password)

root = tk.Tk()
root.geometry('700x600')
root.title('System Administration')

style = Style()

style.configure("TNotebook", background="light grey");
style.map("TNotebook.Tab", background=[("selected", "steel blue")], foreground=[("selected", "white")]);
style.configure("TNotebook.Tab", background="light blue", foreground="black");

tab_control = Notebook(root)
tab1 = Frame(tab_control)
tab2 = Frame(tab_control)
tab3 = Frame(tab_control)
tab4 = Frame(tab_control)
tab5 = Frame(tab_control)
tab6 = Frame(tab_control)
tab7 = Frame(tab_control)

tab_control.add(tab1, text='Grub Management')
tab_control.add(tab2, text='Add User')
tab_control.add(tab3, text='CPU and Memory Usage')
tab_control.add(tab4, text='Nice Values')
tab_control.add(tab5, text='Umask Calulator')
tab_control.add(tab6, text='Default Permissions')
tab_control.add(tab7, text='Managing Log Files')

# Change default operating system
label1 = Label(tab1, text="Set Default Operating System")
label1.grid(column=1, row=1, padx=50, pady=10, sticky="w")
osCombo = Combobox(tab1)
osCombo['values'] = ('Ubuntu', 'Windows')
osCombo.current(0)
osCombo.grid(column=2, row=1, padx=10, pady=10, sticky="w")
changeOsOrderButton = Button(tab1, text="Update", command=change_default_os)
changeOsOrderButton.grid(column=3, row=1, padx=10, pady=10, sticky="w")

# Grub timeout
labelTimeoutPeriod = Label(tab1, text="Set GRUB time-out (seconds)")
grubTimeOutSpin = tk.Spinbox(tab1, from_=0, to=100)
setGrubTimeoutButton = Button(tab1, text="Update", command=set_grub_timeout)
labelTimeoutPeriod.grid(column=1, row=2, padx=50, pady=10, sticky="w")
grubTimeOutSpin.grid(column=2, row=2, padx=10, pady=10, sticky="w")
setGrubTimeoutButton.grid(column=3, row=2, padx=10, pady=10, sticky="w")

# Splash Screen Color
labelSplashScreenColor = Label(tab1, text="Change boot splash screen color")
splashColorButton = Button(tab1, text="Pick Color", command=change_splash_color)
labelSplashScreenColor.grid(column=1, row=3, padx=50, pady=10, sticky="w")
splashColorButton.grid(column=2, row=3, padx=10, pady=10, sticky="w")

# Splash Screen logo
labelSplashLogo = Label(tab1, text="Change boot Splash screen logo")
splashLogoButton = Button(tab1, text="Pick Logo", command=change_splash_logo)
labelSplashLogo.grid(column=1, row=4, padx=50, pady=10, sticky="w")
splashLogoButton.grid(column=2, row=4, padx=10, pady=10, sticky="w")

# Schedule Shutdown and Restart
scheduleShutdownButton = Button(tab1, text="Schedule Shutdown", command=schedule_shutdown)
scheduleShutdownButton.grid(column=1, row=6, padx=50, pady=10, sticky="w")

scheduleRestartButton = Button(tab1, text="Schedule Restart", command=schedule_restart)
scheduleRestartButton.grid(column=2, row=6, padx=50, pady=10, sticky="w")

# Adding User
addUserLable = Label(tab2, text='Add new User to System')
addUserLable.grid(column=1, row=0, padx=50, pady=20, sticky="w")

userNameLabel = Label(tab2, text='User Name')
userNameLabel.grid(column=1, row=1, padx=50, pady=10, sticky="w")
userName = Entry(tab2, width=20)
userName.grid(column=2, row=1, padx=10, pady=10, sticky="w")

passwdLabel = Label(tab2, text='Password')
passwdLabel.grid(column=1, row=2, padx=50, pady=10, sticky="w")
passwd = Entry(tab2, width=20, show='*')
passwd.grid(column=2, row=2, padx=10, pady=10, sticky="w")

confpPasswdLabel = Label(tab2, text='Confirm Password')
confpPasswdLabel.grid(column=1, row=3, padx=50, pady=10, sticky="w")
confPasswd = Entry(tab2, width=20, show='*')
confPasswd.grid(column=2, row=3, padx=10, pady=10, sticky="w")

# shells present in my machine
new_shell = tk.StringVar()
cwd_shell = os.getcwd()
subprocess.call(cwd_shell + '/shell.sh')

shell_data = pd.read_csv("shell.csv")
sdf = pd.DataFrame(shell_data)
shell_mat = []
for row in sdf.iterrows():
    shell_mat.append(row)
range_lenth = len(shell_mat)
shell = []
for i in range(0, range_lenth):
    shell.append(shell_mat[i][1][0])

print(shell)


# on change dropdown value
def change_dropdown2(*args):
    print(new_shell.get())


# link function to change dropdown
new_shell.trace('w', change_dropdown2)

new_shell.set('-Select-')
choices2 = shell

selectShellLabel = Label(tab2, text='Select Shell')
selectShellLabel.grid(column=1, row=4, padx=50, pady=10, sticky="w")
DropDown2 = OptionMenu(tab2, new_shell, *choices2)
DropDown2.grid(column=2, row=4, padx=20, pady=10, sticky="w")

addUserButton = Button(tab2, text='Add User', command=add_user)
addUserButton.grid(column=2, row=5, padx=50, pady=10, sticky="w")

addUsersLabel = Label(tab2, text='Add Multiple Users')
addUsersLabel.grid(column=1, row=7, padx=50, pady=50, sticky="w")

addUsersButton = Button(tab2, text='Select csv file', command=add_user_batch)
addUsersButton.grid(column=2, row=7, padx=10, pady=10, sticky="w")


#delete User
def del_user():
    username = simpledialog.askstring("Delete USER", "Enter Username ", parent=tab2)
    username2 = simpledialog.askstring("Delete USER", "Confirm Username ", parent=tab2)

    if username != "" and username == username2:
        cmd1 = "echo \"" + password + "\" | sudo -S userdel -r \"" + username + "\""
        print(cmd1)
        subprocess.call(cmd1, shell=True)
        messagebox.showinfo("Delete User", "Successfully Deleted")
        print("done")
    else:
        messagebox.showwarning("WARNING", "Username not matched")


#lock User
def lock_user():
    username = simpledialog.askstring("Lock USER", "Enter Username ", parent=tab2)
    username2 = simpledialog.askstring("Lock USER", "Confirm Username ", parent=tab2)

    if username != "" and username == username2:
        cmd1 = "echo \"" + password + "\" | sudo -S usermod -L \"" + username + "\""
        print(cmd1)
        subprocess.call(cmd1, shell=True)
        messagebox.showinfo("Lock User", "Successfully Locked")
        print("done")
    else:
        messagebox.showwarning("WARNING", "Username not matched")


#unlock User
def unlock_user():
    username = simpledialog.askstring("Unlock USER", "Enter Username ", parent=tab2)
    username2 = simpledialog.askstring("Unlock USER", "Confirm Username ", parent=tab2)

    if username != "" and username == username2:
        cmd1 = "echo \"" + password + "\" | sudo -S usermod --unlock \"" + username + "\""
        print(cmd1)
        subprocess.call(cmd1, shell=True)
        messagebox.showinfo("Unlock User", "Successfully Unlocked")
        print("done")
    else:
        messagebox.showwarning("WARNING", "Username not matched")


#update username
def update_username():
    username = simpledialog.askstring("Update Username", "Enter Username ", parent=tab2)
    new_username = simpledialog.askstring("Update Username", "Enter New Username ", parent=tab2)
    new_username2 = simpledialog.askstring("Update Username", "Confirm New Username ", parent=tab2)

    if username != "" and new_username == new_username2:
        cmd1 = "echo \"" + password + "\" | sudo -S usermod -l \"" + new_username + "\" \"" + username + "\""
        print(cmd1)
        subprocess.call(cmd1, shell=True)
        messagebox.showinfo("Update Username", "Successfully Updated Username")
        print("done")
    else:
        messagebox.showwarning("WARNING", "Username not matched")


#update user's Shell
def update_usershell():
    username = simpledialog.askstring("Update user's shell", "Enter Username ", parent=tab2)
    user_sh = simpledialog.askstring("Update user's shell", "Enter new Usershell ", parent=tab2)
    user_sh2 = simpledialog.askstring("Update user's shell", "Confirm Usershell ", parent=tab2)

    if username != "" and user_sh == user_sh2:
        cmd1 = "echo \"" + password + "\" | sudo -S usermod -s \"" + user_sh + "\" \"" + username + "\""
        print(cmd1)
        subprocess.call(cmd1, shell=True)
        messagebox.showinfo("Update User's Shell", "Successfully Updated User's Shell")
        print("done")
    else:
        messagebox.showwarning("WARNING", "Usershell not matched")


#update user's uid
def update_userUID():
    username = simpledialog.askstring("Update user's UID", "Enter Username ", parent=tab2)
    user_uid = simpledialog.askstring("Update user's UID", "Enter new UID ", parent=tab2)
    user_uid2 = simpledialog.askstring("Update user's UID", "Confirm new UID ", parent=tab2)

    if username != "" and user_uid == user_uid2:
        cmd1 = "echo \"" + password + "\" | sudo -S usermod -u \"" + user_uid + "\" \"" + username + "\""
        print(cmd1)
        subprocess.call(cmd1, shell=True)
        messagebox.showinfo("Update User's UID", "Successfully Updated User's UID")
        print("done")
    else:
        messagebox.showwarning("WARNING", "User's UID not matched")


#update user's gid
def update_userGID():
    username = simpledialog.askstring("Update user's GID", "Enter Username ", parent=tab2)
    user_gid = simpledialog.askstring("Update user's GID", "Enter new GID ", parent=tab2)
    user_gid2 = simpledialog.askstring("Update user's GID", "Confirm new GID ", parent=tab2)

    if username != "" and user_gid == user_gid2:
        cmd1 = "echo \"" + password + "\" | sudo -S groupmod -g \"" + user_gid + "\" \"" + username + "\""
        cmd2 = "echo \"" + password + "\" | sudo -S usermod -g \"" + user_gid + "\" \"" + username + "\""
        print(cmd2)
        print(cmd1)
        subprocess.call(cmd1, shell=True)
        subprocess.call(cmd2, shell=True)
        messagebox.showinfo("Update User's GID", "Successfully Updated User's GID")
        print("done")
    else:
        messagebox.showwarning("WARNING", "User's GID not matched")


#update user's homedir
def update_homedir():
    username = simpledialog.askstring("Update user's Home Dir", "Enter Username ", parent=tab2)
    user_dir = simpledialog.askstring("Update user's Home Dir", "Enter new User's Home Dir ", parent=tab2)
    user_dir2 = simpledialog.askstring("Update user's Home Dir", "Confirm new User's Home Dir ", parent=tab2)

    if username != "" and user_dir == user_dir2:
        cmd1 = "echo \"" + password + "\" | sudo -S mkdir -p \"" + user_dir + "\""
        cmd2 = "echo \"" + password + "\" | sudo -S usermod -d \"" + user_dir + "\" \"" + username + "\""
        print(cmd2)
        print(cmd1)
        subprocess.call(cmd1, shell=True)
        subprocess.call(cmd2, shell=True)
        messagebox.showinfo("Update User's Home Dir", "Successfully Updated User's Home Dir")
        print("done")
    else:
        messagebox.showwarning("WARNING", "User's Home Dir not matched")


#set Expiry Date
def setExd():
    username = simpledialog.askstring("Set Expiry Date", "Enter Username ", parent=tab2)
    user_exd = simpledialog.askstring("Set Expiry Date", "Enter Expiry Date ", parent=tab2)
    user_exd2 = simpledialog.askstring("Set Expiry Date", "Confirm Expiry Date ", parent=tab2)

    if username != "" and user_exd == user_exd2:
        cmd = "echo \"" + password + "\" | sudo -S usermod -e \"" + user_exd + "\" \"" + username + "\""
        print(cmd)
        subprocess.call(cmd, shell=True)
        messagebox.showinfo("Set Expiry Date", "Successfully Updated Expiry Date")
        print("done")
    else:
        messagebox.showwarning("WARNING", "Expiry Date not matched")


#Change Password
def setPwd():
    username = simpledialog.askstring("Change Password", "Enter Username ", parent=tab2)
    user_pxd = simpledialog.askstring("Change Password", "Enter Password ", parent=tab2)
    user_pxd2 = simpledialog.askstring("Change Password", "Confirm Password ", parent=tab2)

    if username != "" and user_pxd == user_pxd2:
        cmd = "echo \"" + username + ":" + user_pxd + "\" | sudo chpasswd -c SHA512"
        print(cmd)
        subprocess.call(cmd, shell=True)
        messagebox.showinfo("Change Password", "Successfully Updated Password")
        print("done")
    else:
        messagebox.showwarning("WARNING", "Password not matched")


deleteUserButton = Button(tab2, text="Delete User", command=del_user)
deleteUserButton.grid(column=4, row=1, padx=10, pady=10, sticky="w,e")

updateUserNameButton = Button(tab2, text="Update UserName", command=update_username)
updateUserNameButton.grid(column=4, row=2, padx=10, pady=10, sticky="w,e")

LockUserButton = Button(tab2, text="Update Password", command=setPwd)
LockUserButton.grid(column=4, row=3, padx=10, pady=10, sticky="w,e")

updateUserShellButton = Button(tab2, text="Update User Shell", command=update_usershell)
updateUserShellButton.grid(column=4, row=4, padx=10, pady=10, sticky="w,e")

LockUserButton = Button(tab2, text="Lock User", command=lock_user)
LockUserButton.grid(column=4, row=5, padx=10, pady=10, sticky="w,e")

LockUserButton = Button(tab2, text="Unlock User", command=unlock_user)
LockUserButton.grid(column=4, row=6, padx=10, pady=10, sticky="w,e")

LockUserButton = Button(tab2, text="Delete User", command=lock_user)
LockUserButton.grid(column=4, row=7, padx=10, pady=10, sticky="w,e")





# Pie Charts

cpuUsageLabel = Label(tab3, text="CPU Usage")
cpuUsageLabel.grid(column=1, row=1, padx=50, pady=10, sticky="w")

memoryUsageUpdateButton = Button(tab3, text='Update', command=update_cpu_usage)
memoryUsageUpdateButton.grid(column=1, row=2, padx=50, pady=10, sticky="w")

memoryUsageLabel = Label(tab3, text="Memory Usage")
memoryUsageLabel.grid(column=5, row=1, padx=50, pady=10, sticky="w")

memoryUsageUpdateButton = Button(tab3, text='Update', command=update_memory_usage)
memoryUsageUpdateButton.grid(column=5, row=2, padx=50, pady=10, sticky="w")

update_memory_usage()
update_cpu_usage()

# Updating Nice values

nicevalue1 = tk.IntVar()
nicevalue2 = tk.IntVar()
nicevalue3 = tk.IntVar()
nicevalue4 = tk.IntVar()
nicevalue5 = tk.IntVar()


def update_nicetable():
    cwd = os.getcwd()
    subprocess.call(cwd+'/nicevalue.sh')

    arr = []

    f = open("nice.txt","r")
    for ele in f:
        arr.append(ele.split(' '))
    f.close()

    for i in range(len(arr)):
        arr[i][3] = arr[i][3].strip('\n')

    print(arr)

    def update_nicevalue1():
        nice = nicevalue1.get()
        if -20 <= nice <= 19:
            cmd = "echo \"" + password + "\" | sudo -S renice " + str(nice) + " " + arr[0][0]
            print(cmd)
            subprocess.call(cmd, shell=True)
            messagebox.showinfo("Update Nice Value", "Successfully Updated")
        else:
            messagebox.showwarning("WARNING", "Enter nice value between -20 to 19 only")


    def update_nicevalue2():
        nice = nicevalue2.get()
        if -20 <= nice <= 19:
            cmd = "echo \"" + password + "\" | sudo -S renice " + str(nice) + " " + arr[1][0]
            print(cmd)
            subprocess.call(cmd, shell=True)
            messagebox.showinfo("Update Nice Value", "Successfully Updated")
        else:
            messagebox.showwarning("WARNING", "Enter nice value between -20 to 19 only")


    def update_nicevalue3():
        nice = nicevalue3.get()
        if -20 <= nice <= 19:
            cmd = "echo \"" + password + "\" | sudo -S renice " + str(nice) + " " + arr[2][0]
            print(cmd)
            subprocess.call(cmd, shell=True)
            messagebox.showinfo("Update Nice Value", "Successfully Updated")
        else:
            messagebox.showwarning("WARNING", "Enter nice value between -20 to 19 only")


    def update_nicevalue4():
        nice = nicevalue4.get()
        if -20 <= nice <= 19:
            cmd = "echo \"" + password + "\" | sudo -S renice " + str(nice) + " " + arr[3][0]
            print(cmd)
            subprocess.call(cmd, shell=True)
            messagebox.showinfo("Update Nice Value", "Successfully Updated")
        else:
            messagebox.showwarning("WARNING", "Enter nice value between -20 to 19 only")


    def update_nicevalue5():
        nice = nicevalue5.get()
        if -20 <= nice <= 19:
            cmd = "echo \"" + password + "\" | sudo -S renice " + str(nice) + " " + arr[4][0]
            print(cmd)
            subprocess.call(cmd, shell=True)
            messagebox.showinfo("Update Nice Value", "Successfully Updated")
        else:
            messagebox.showwarning("WARNING", "Enter nice value between -20 to 19 only")

    nicenessLabel = Label(tab4, text="Change Niceness for top 5 processes")
    nicenessLabel.grid(column=0, row=0, columnspan=3, padx=10, pady=50, sticky="w")

    niceheadLabel1 = Label(tab4, text="process ID", justify=LEFT)
    niceheadLabel1.grid(column=0, row=1, padx=10, pady=10, sticky="w")
    niceheadLabel2 = Label(tab4, text="Scheduling Priority", justify=LEFT)
    niceheadLabel2.grid(column=1, row=1, padx=10, pady=10, sticky="w")
    niceheadLabel3 = Label(tab4, text="Niceness value", justify=LEFT)
    niceheadLabel3.grid(column=2, row=1, padx=10, pady=10, sticky="w")
    niceheadLabel4 = Label(tab4, text="Update Niceness", justify=LEFT)
    niceheadLabel4.grid(column=3, row=1, padx=10, pady=10, sticky="w")

    x_value = 20
    y_value = 140
    for i in range(0, len(arr)):
        Label(tab4, text=arr[i][0], justify=LEFT).grid(column=0, row=2+i, padx=10, pady=10)
        Label(tab4, text=arr[i][1], justify=LEFT).grid(column=1, row=2+i, padx=10, pady=10)
        Label(tab4, text=arr[i][2], justify=LEFT).grid(column=2, row=2+i, padx=10, pady=10)
        y_value += 50

    E1 = Entry(tab4, textvariable=nicevalue1).grid(column=3, row=2, padx=10, pady=10, sticky="w")
    E2 = Entry(tab4, textvariable=nicevalue2).grid(column=3, row=3, padx=10, pady=10, sticky="w")
    E3 = Entry(tab4, textvariable=nicevalue3).grid(column=3, row=4, padx=10, pady=10, sticky="w")
    E4 = Entry(tab4, textvariable=nicevalue4).grid(column=3, row=5, padx=10, pady=10, sticky="w")
    E5 = Entry(tab4, textvariable=nicevalue5).grid(column=3, row=6, padx=10, pady=10, sticky="w")
    But1 = Button(tab4, text="Update", command=update_nicevalue1).grid(column=4, row=2, padx=10, pady=10, sticky="w")
    But2 = Button(tab4, text="Update", command=update_nicevalue2).grid(column=4, row=3, padx=10, pady=10, sticky="w")
    But3 = Button(tab4, text="Update", command=update_nicevalue3).grid(column=4, row=4, padx=10, pady=10, sticky="w")
    But4 = Button(tab4, text="Update", command=update_nicevalue4).grid(column=4, row=5, padx=10, pady=10, sticky="w")
    But5 = Button(tab4, text="Update", command=update_nicevalue5).grid(column=4, row=6, padx=10, pady=10, sticky="w")


update_nicetable()
reset_niceness_button = Button(tab4, text="Reset", command=update_nicetable).grid(column=2, row=8, pady=20, sticky="w")




# U Mask Calculator
def getUnmaskFile():
    m1 = filemasku.get()
    m2 = filemaskg.get()
    m3 = filemasko.get()
    #default value
    default = ["---","--x","-w-","-wx","r--","r-x","rw-", "rwx"]
    value = [4,2,1]

    if m1 not in default or m2 not in default or m3 not in default:
        messagebox.showwarning("WARNING", "Enter Right Values")
    else:
        m1 = list(m1)
        m2 = list(m2)
        m3 = list(m3)

        count1=0
        count2=0
        count3=0

        for i in range(0,3):
            if m1[i] == "-":
               count1 = count1+value[i]
            if m2[i] == "-":
               count2 = count2+value[i]
            if m3[i] == "-":
               count3 = count3+value[i]

        if count1 == 7:
            p1 = default[0]
        else:
            p1 = default[6-count1]

        if count2 == 7:
            p2 = default[0]
        else:
            p2 = default[6-count2]

        if count3 == 7:
            p3 = default[0]
        else:
            p3 = default[6-count3]

        defaultFilePermission.config(text=p1+" "+p2+" "+p3)
        messagebox.showinfo("Umask", "Successfully Updated")


def getUnmaskDir():
    m1 = directorymasku.get()
    m2 = directorymaskg.get()
    m3 = directorymasko.get()
    #default value
    default = ["---","--x","-w-","-wx","r--","r-x","rw-", "rwx"]
    value = [4,2,1]

    if m1 not in default or m2 not in default or m3 not in default:
        messagebox.showwarning("WARNING", "Enter Right Values")
    else:
        m1 = list(m1)
        m2 = list(m2)
        m3 = list(m3)

        count1=0
        count2=0
        count3=0

        for i in range(0,3):
            if m1[i] == "-":
               count1 = count1+value[i]
            if m2[i] == "-":
               count2 = count2+value[i]
            if m3[i] == "-":
               count3 = count3+value[i]

        p1 = default[7-count1]
        p2 = default[7-count2]
        p3 = default[7-count3]

        defaultdirectoryPermission.config(text=p1+" "+p2+" "+p3)
        messagebox.showinfo("Umask", "Successfully Updated")

regularFileLabel = Label(tab5, text="Regular File Permissios")
regularFileLabel.grid(column=1, row=0, padx=10, pady=30, sticky="w")

enterfileumasklabel = Label(tab5, text="Enter Umask Value")
enterfileumasklabel.grid(column=1, row=1, padx=10, pady=10, sticky="w")

filemasku = Entry(tab5, width=10)
filemasku.grid(column=2, row=1, padx=5, pady=10, sticky="w")

filemaskg = Entry(tab5, width=10)
filemaskg.grid(column=3, row=1, padx=5, pady=10, sticky="w")

filemasko = Entry(tab5, width=10)
filemasko.grid(column=4, row=1, padx=5, pady=10, sticky="w")

submitFileMaskButton = Button(tab5, text="Submit", command=getUnmaskFile)
submitFileMaskButton.grid(column=2, row=2, padx=10, pady=10, sticky="w")

defaultFilepermissionLabel = Label(tab5, text="Default File Permissions")
defaultFilepermissionLabel.grid(column=1, row=3, padx=10, pady=10, sticky="w")

defaultFilePermission = Label(tab5, text="submit umask")
defaultFilePermission.grid(column=2, row=3, padx=10, pady=10, sticky="w")


directoryLabel = Label(tab5, text="Directory Permissions")
directoryLabel.grid(column=1, row=4, padx=10, pady=30, sticky="w")

enterdirectoryumasklabel = Label(tab5, text="Enter Umask Value")
enterdirectoryumasklabel.grid(column=1, row=5, padx=10, pady=10, sticky="w")

directorymasku = Entry(tab5, width=10)
directorymasku.grid(column=2, row=5, padx=5, pady=10, sticky="w")

directorymaskg = Entry(tab5, width=10)
directorymaskg.grid(column=3, row=5, padx=5, pady=10, sticky="w")

directorymasko = Entry(tab5, width=10)
directorymasko.grid(column=4, row=5, padx=5, pady=10, sticky="w")

submitdirectoryMaskButton = Button(tab5, text="Submit", command=getUnmaskDir)
submitdirectoryMaskButton.grid(column=2, row=6, padx=10, pady=10, sticky="w")

defaultdirectorypermissionLabel = Label(tab5, text="Default Directory Permissions")
defaultdirectorypermissionLabel.grid(column=1, row=7, padx=10, pady=10, sticky="w")

defaultdirectoryPermission = Label(tab5, text="submit umask")
defaultdirectoryPermission.grid(column=2, row=7, padx=10, pady=10, sticky="w")




# Default Permissions


def setFile():
    global filename
    prmxn = newFilePermissions.get()
    cmd = "echo \"" + password + "\" | sudo -S chmod " + prmxn + " " + filename
    print(cmd)
    subprocess.call(cmd, shell=True)
    messagebox.showinfo("Default Permissions", "Successfully Done")


def setDir():
    filename = selectDirectoryEntry.get()
    prmxn = newDirectoryPermissions.get()
    cmd = "echo \"" + password + "\" | sudo -S chmod " + prmxn + " " + filename
    print(cmd)
    subprocess.call(cmd, shell=True)
    messagebox.showinfo("Default Permissions", "Successfully Done")


filename = ""
def pickfile():
    global filename
    file_path = filedialog.askopenfilename(initialdir="/home", title="Select file")
    selectedFileLabel.config(text=file_path)
    filename = file_path


filePermissionLabel = Label(tab6, text="Change File Permissions")
filePermissionLabel.grid(column=0, row=0, padx=10, pady=20, sticky="w")

selectfilelabel = Label(tab6, text="Select File")
selectfilelabel.grid(column=0, row=1, padx=10, pady=10, sticky="w")

selectFileButton = Button(tab6, text="Pick File", command=pickfile)
selectFileButton.grid(column=1, row=1, padx=10, pady=10, sticky="w")

selectedFileLabel = Label(tab6, text="No file selected")
selectedFileLabel.grid(column=2, row=1, padx=10, pady=10, sticky="w")

newFilePermissionLabel = Label(tab6, text="Enter New Permissions")
newFilePermissionLabel.grid(column=0, row=2, padx=10, pady=10, sticky="w")

newFilePermissions = Entry(tab6, width=20)
newFilePermissions.grid(column=1, row=2, padx=10, pady=10, sticky="w")

updateFilePermissionButton = Button(tab6, text="Update", command=setFile)
updateFilePermissionButton.grid(column=1, row=3, padx=10, pady=10, sticky="w")



directoryPermissionLabel = Label(tab6, text="Change Directory Permissions")
directoryPermissionLabel.grid(column=0, row=4, padx=10, pady=20, sticky="w")

selectdirectorylabel = Label(tab6, text="Enter Directory path")
selectdirectorylabel.grid(column=0, row=5, padx=10, pady=10, sticky="w")
selectDirectoryEntry = Entry(tab6, width=20)
selectDirectoryEntry.grid(column=1, row=5, padx=10, pady=10, sticky="w")

newFilePermissionLabel = Label(tab6, text="Enter New Permissions")
newFilePermissionLabel.grid(column=0, row=6, padx=10, pady=10, sticky="w")

newDirectoryPermissions = Entry(tab6, width=20)
newDirectoryPermissions.grid(column=1, row=6, padx=10, pady=10, sticky="w")

updateDirectoryPermissionButton = Button(tab6, text="Update", command=setDir)
updateDirectoryPermissionButton.grid(column=1, row=7, padx=10, pady=10, sticky="w")




# Managing Log Files
facility = ["*", "kern", "user", "mail", "daemon", "auth", "syslog", "lpr", "news", "cron", "authprev", "ftp", "mark", "local0", "local1", "local2", "local3", "local4", "local5","local6", "local7"]
levels = ["*", "none", "emerg", "alert", "crit", "err", "warning", "notice", "info", "debug"]

def setlog():
    fac = facilityCombo.get()
    lev = levelCombo.get()
    fileName = logFileName.get()

    cmd = "echo \"" + password + "\" | sudo -S touch " + fileName
    print(cmd)
    subprocess.call(cmd, shell=True)

    logline = fac + "." + "=" + lev + "    " + fileName
    cwd = os.getcwd()

    cmd2 = "chmod 777 manageLog.sh"
    subprocess.call(cmd2, shell=True)

    cmd3 = "echo \"" + password + "\" | sudo -S ./manageLog.sh " + logline
    print(cmd3)
    subprocess.call(cmd3, shell=True)
    messagebox.showinfo("Manage Log files", "Successfully Done")


manageLogFilesLabel = Label(tab7, text="Managing Log Files")
manageLogFilesLabel.grid(column=0, row=0, padx=20, pady=20, columnspan=2)

facilityLabel = Label(tab7, text="Facility")
facilityLabel.grid(column=0, row=1, padx=10, pady=10, sticky="w")

facilityCombo = Combobox(tab7)
facilityCombo['values'] = ("*", "kern", "user", "mail", "daemon", "auth", "syslog", "lpr", "news", "cron", "authprev", "ftp", "mark", "local0", "local1", "local2", "local3", "local4", "local5","local6", "local7")
facilityCombo.current(0)
facilityCombo.grid(column=1, row=1, padx=10, pady=10, sticky="w")


levelLabel = Label(tab7, text="Severity Level")
levelLabel.grid(column=0, row=2, padx=10, pady=10, sticky="w")

levelCombo = Combobox(tab7)
levelCombo['values'] = ("none", "emerg", "alert", "crit", "err", "warning", "notice", "info", "debug")
levelCombo.current(0)
levelCombo.grid(column=1, row=2, padx=10, pady=10, sticky="w")

logFileNameLabel = Label(tab7, text="Enter log file name")
logFileNameLabel.grid(column=0, row=3, padx=10, pady=10, sticky="w")

logFileName = Entry(tab7, width=20)
logFileName.grid(column=1, row=3, padx=10, pady=10, sticky="w")

createLogButton = Button(tab7, text="Submit", command=setlog)
createLogButton.grid(column=1, row=4, padx=10, pady=20, sticky="w")



tab_control.pack(expand=1, fill='both')
root.mainloop()
