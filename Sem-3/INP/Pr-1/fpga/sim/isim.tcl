proc isim_script {} {

   add_divider "Signals of the Vigenere Interface"
   add_wave_label "" "CLK" /testbench/clk
   add_wave_label "" "RST" /testbench/rst
   add_wave_label "-radix ascii" "DATA" /testbench/tb_data
   add_wave_label "-radix ascii" "KEY" /testbench/tb_key
   add_wave_label "-radix ascii" "CODE" /testbench/tb_code

   add_divider "Vigenere Inner Signals"
   add_wave_label "" "state" /testbench/uut/state
   # sem doplnte vase vnitrni signaly. chcete-li v diagramu zobrazit desitkove
   # cislo, vlozte do prvnich uvozovek: -radix dec
   add_wave_label "-radix dec" "SHIFT" /testbench/uut/SHIFT
   add_wave_label "-radix ascii" "PLUS" /testbench/uut/PLUS
   add_wave_label "-radix ascii" "MINUS" /testbench/uut/MINUS   

   add_wave_label "" "FSM_OUTPUT" /testbench/uut/FSM_OUTPUT
   add_wave_label "" "P_STATE" /testbench/uut/P_STATE
   add_wave_label "" "N_STATE" /testbench/uut/N_STATE
   run 8 ns
}
