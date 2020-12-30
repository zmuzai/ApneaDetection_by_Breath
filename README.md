# ApneaDetection_by_Breath

This code is based on the algorithm described in the following papers with some improvements.   
If you want use this code, please cite the paper:  
@article{2018Apnea,
  title={Apnea and heart rate detection from tracheal body sounds for the diagnosis of sleep-related breathing disorders},  
  author={ Kalkbrenner, Christoph  and  Eichenlaub, Manuel  and Stefan Rüdiger and  Kropf-Sanchen, Cornelia  and  Rottbauer, Wolfgang  and  Brucher, Rainer },  
  journal={Medical & Biological Engineering & Computing},  
  volume={56},  
  number={4},  
  pages={671-681},  
  year={2018},  
}


The algorithm is as follows：
1.	数据预处理  
  a)	去除任何心音和噪音，并产生一个主要包含呼吸音的信号  
  b)	使用200-2000Hz之间的FIR带通滤波器  
  c)	为了消除背景噪声对安静呼吸声检测的影响，采用谱减法滤波技术  
2.	降低检测  
  a)	阶段目标：扫描整个信号呼吸音振幅的下降，识别出可能的呼吸暂停信号  
  b)	首先，计算预处理后短时窗口内音频信号的平均强度，提取代表每个呼吸周期的包络曲线E1  
    i.	短时窗口：每个点，论文中麦克风为5kHz  
    ii.	用来画呼吸线  
  c)	使用一个长期窗口标准差计算的自适应阈值来切断由于打鼾带来的离群值  
    i.	我们的数据集是30s，长期窗口标准差可以设置为30s  
  d)	通过在第一包络线E1中插值单次呼吸周期的局部最大值来使用分段三次Her-mite插值实现E2包络线  
    i.	E2包络线就是取E1最大值点平滑连接  
  e)	自适应阈值之下的E2包络线的所有信号片段被识别为呼吸幅度下降  
  f)	最终，这些点和他们直接相邻的片段被提取为可能的呼吸暂停片段。  
  

