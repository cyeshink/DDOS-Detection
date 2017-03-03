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

namespace WindowsFormsApplication1
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            Stack<TreeNode> DisplayNodes = new Stack<TreeNode>();
            InitializeComponent();
            this.KeyPreview = true;
            this.KeyPress +=
                new KeyPressEventHandler(Form1_KeyPress);
            messageGeneratedFontSize.Value = 10;
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
                useFile(openAnalysisFileDialog.FileName);
            }
        }

        private void useFile(string filename)
        {
            filename = filename.ToLower();
            var lines = File.ReadLines(filename);
            int lineNumber = lines.Count();
            for (int i = 0; i < lineNumber; i++)
            {
                if (filename.Contains(".daf"))//parse DAF file if it's daf file
                {
                    TreeNode root = displayString(lines.ElementAt(i), null);
                    if (lineNumber % 2 == 0)
                    {
                        TreeNode level1 = displayString(lines.ElementAt(++i), root);
                    }
                }
                //call python analysis method if it's txt file and display it in tiers
                /*WIP
                if (filename.Contains(".txt"))
                {
                    System.Diagnostics.Process process = new System.Diagnostics.Process();
                    System.Diagnostics.ProcessStartInfo startInfo = new System.Diagnostics.ProcessStartInfo();
                    startInfo.WindowStyle = System.Diagnostics.ProcessWindowStyle.Hidden;
                    startInfo.FileName = "python.exe";
                    startInfo.Arguments = "-c import ddosanalysis; ddosanalysis.process(filename)";
                    process.StartInfo = startInfo;
                    process.Start();
                    //after program has analyzed log and made .daf file
                    string newFileName = filename.strip(".txt");
                    useFile(newFileName);
                }*/

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
    }

}

