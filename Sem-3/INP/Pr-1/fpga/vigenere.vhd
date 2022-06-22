library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.std_logic_arith.all;
use IEEE.std_logic_unsigned.all;

-- rozhrani Vigenerovy sifry
entity vigenere is
   port(
         CLK : in std_logic;
         RST : in std_logic;
         DATA : in std_logic_vector(7 downto 0);
         KEY : in std_logic_vector(7 downto 0);

         CODE : out std_logic_vector(7 downto 0)
    );
end vigenere;


architecture behavioral of vigenere is
	signal SHIFT : std_logic_vector(7 downto 0);
	signal PLUS : std_logic_vector(7 downto 0);
	signal MINUS : std_logic_vector(7 downto 0);
	
	signal FSM_OUTPUT : std_logic_vector(1 downto 0);
	
	type FSMstate is (doPlus, doMinus);
	signal P_STATE : FSMstate;
	signal N_STATE : FSMstate;
	
begin
    -- Sem doplnte popis obvodu. Doporuceni: pouzivejte zakladni obvodove prvky
    -- (multiplexory, registry, dekodery,...), jejich funkce popisujte pomoci
    -- procesu VHDL a propojeni techto prvku, tj. komunikaci mezi procesy,
    -- realizujte pomoci vnitrnich signalu deklarovanych vyse.

    -- DODRZUJTE ZASADY PSANI SYNTETIZOVATELNEHO VHDL KODU OBVODOVYCH PRVKU,
    -- JEZ JSOU PROBIRANY ZEJMENA NA UVODNICH CVICENI INP A SHRNUTY NA WEBU:
    -- http://merlin.fit.vutbr.cz/FITkit/docs/navody/synth_templates.html.

	shift_proc: process(DATA, KEY) is
	begin
		SHIFT <= KEY - 64;
	end process;

	plus_proc: process(DATA, SHIFT) is
		variable tmp : std_logic_vector(7 downto 0);
	begin
		tmp := DATA;
		tmp := tmp + SHIFT;
		if (tmp > 90) then
			tmp := tmp - 26;
		end if;
		PLUS <= tmp;
	end process;

	minus_proc: process(DATA, SHIFT) is
		variable tmp : std_logic_vector(7 downto 0);
	begin
		tmp := DATA;
		tmp := tmp - SHIFT;
		if (tmp < 65) then
			tmp := tmp + 26;
		end if;
		MINUS <= tmp;
	end process;
	
	fsm_pstate: process(DATA, CLK, RST) is
	begin
		if (RST = '1') then
			P_STATE <= doPlus;
		elsif rising_edge(CLK) then
			P_STATE <= N_STATE;
		end if;
	end process;

	fsm_nstate: process(DATA, RST, P_STATE) is
	begin
		case P_STATE is
			when doPlus =>
				N_STATE <= doMinus;
				FSM_OUTPUT <= "01";
			when doMinus =>
				N_STATE <= doPlus;
				FSM_OUTPUT <= "10";
			when others => null;
		end case;
		if (RST = '1') or ((DATA > 47) and (DATA < 58)) then
			FSM_OUTPUT <= "00";
		end if;
	end process;
	
	CODE <= PLUS when (FSM_OUTPUT = "01") else
			  MINUS when (FSM_OUTPUT = "10") else
			  "00100011";
end behavioral;
