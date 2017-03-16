using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;
using IronPython.Hosting;
using Microsoft.Scripting.Hosting;

namespace WindowsFormsApplication1
{
    public partial class Form1 : Form
    {
        string helpfilename = "../../../../README.md";
        string filepath = "";
        int maxEntries = 0;
        public Form1()
        {
            //Stack<TreeNode> DisplayNodes = new Stack<TreeNode>();
            InitializeComponent();
            this.KeyPreview = true;
            this.KeyPress +=
                new KeyPressEventHandler(Form1_KeyPress);
            messageGeneratedFontSize.Value = 10;
            maxEntries = 0;
            //TreeNode DDOS1_L1 = messageGeneratedTreeView.Nodes.Add("DDOS1 : <Example IP1>");
            //TreeNode DDOS1_L2 = DDOS1_L1.Nodes.Add("DDOS1 : More Info displayed here...");
            //TreeNode DDOS2_L1 = messageGeneratedTreeView.Nodes.Add("DDOS2 : <Example IP2>");
            //TreeNode DDOS2_L2 = DDOS2_L1.Nodes.Add("DDOS2 : More Info displayed here...");
        }

        void Form1_KeyPress(object sender, KeyPressEventArgs e)
        {
            if(e.KeyChar == 13)//enter key
            {
                useFile(filePathTextBox.Text);
            }
        }

        private void messageGeneratedTreeView_AfterSelect(object sender, TreeViewEventArgs e)
        {
        }

        private void fileSelectButton_Click(object sender, EventArgs e)
        {
            OpenFileDialog openAnalysisFileDialog = new OpenFileDialog();
            openAnalysisFileDialog.InitialDirectory = "C:\\";
            openAnalysisFileDialog.Filter = "txt files (*.txt)|*.txt|DDOS Analysis Files (*.daf)|*.daf|All files (*.*)|*.*";
            openAnalysisFileDialog.FilterIndex = 2;
            openAnalysisFileDialog.RestoreDirectory = true;

            if(openAnalysisFileDialog.ShowDialog() == DialogResult.OK)
            {
                filepath = openAnalysisFileDialog.FileName /*+ " "*/;
                //messageGeneratedTreeView.Nodes.Clear(); 
                useFile(openAnalysisFileDialog.FileName + " ");
            }
        }

        private void useFile(string filename)
        {
            messageGeneratedTreeView.Nodes.Clear();
            filePathTextBox.Text = filename/*.Substring(0, filename.Length-1)*/;
            Console.WriteLine("useFile called with: " + filename);
            var lines = File.ReadLines(filename);
            int lineNumber = lines.Count();
            int level = 0;
            int count = 0;
            int num = 0;
            if (filename.ToLower().Contains(".daf"))
            {
                int i = 0;
                TreeNode[] TreeNodesByLevel = new TreeNode[10];//allow up to 10 levels
                while (i < lines.Count())
                {
                    string line = lines.ElementAt(i);
                    TreeNode parent = null;//assume root, unless if statement below is true
                    level = findlevel(line);
                    if(level == 0)
                    {
                        count = 0;
                        num = findlevel(lines.ElementAt(++i));
                        if(num > MaxEntriesUpDown.Value)
                        {
                            i += num;
                        }
                    }
                    if(level > 0 && level < TreeNodesByLevel.Length - 1)//child
                    {
                        parent = TreeNodesByLevel[level - 1];
                    }
                    if (level < TreeNodesByLevel.Length)
                    {
                        TreeNodesByLevel[level] = displayString(line, parent);
                    }
                    i++;
                }
            }
            //call python analysis method if it's log file and display it in tiers
            if (filename.ToLower().Contains(".log"))
            {
                var py = Python.CreateEngine();
                var scope = py.CreateScope();

                List<String> argv = new List<String>();
                argv.Add(filename);
                py.GetSysModule().SetVariable("argv", argv);
                try
                {
                    py.ExecuteFile(@"ddosanalysis.py", scope);
                }
                catch(Exception ex)
                {
                    Console.WriteLine("Python exception: " + ex.Message);
                }
                Console.WriteLine("Finished py.executefile");
                string newFileName = filename.Replace(".log", ".daf");
                int wait = 0;
                while (!File.Exists(newFileName))
                {
                    wait++;
                    Console.WriteLine("Wait! " + wait);
                }
                useFile(newFileName);
            }
            //filePathTextBox.Text = filename;
        }
        private TreeNode displayString(string line, TreeNode parent)//parent=null for root
        {
            TreeNode newNode;
            if (parent == null)
            {
                newNode = messageGeneratedTreeView.Nodes.Add(line);
            }
            else
            {
                newNode = parent.Nodes.Add(line);
            }
            return newNode;
        }

        private void filePathTextBox_TextChanged(object sender, EventArgs e)
        {

        }

        private void messageGeneratedFontSize_ValueChanged(object sender, EventArgs e)
        {
            messageGeneratedTreeView.Font = new Font(messageGeneratedTreeView.Font.FontFamily, (Single)messageGeneratedFontSize.Value);
        }

        private int findlevel(string line)
        {
            return Int32.Parse(line.Substring(0, 2));
        }

        private void MaxEntriesUpDown_ValueChanged(object sender, EventArgs e)
        {
            maxEntries = (int)MaxEntriesUpDown.Value;
        }

        private void HelpButton_Click(object sender, EventArgs e)
        {
            Console.WriteLine(System.IO.Directory.GetCurrentDirectory());
            System.Diagnostics.Process.Start("notepad.exe", helpfilename);
        }
    }

}

