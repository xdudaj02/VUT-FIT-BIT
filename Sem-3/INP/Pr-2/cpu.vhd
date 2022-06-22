-- cpu.vhd: Simple 8-bit CPU (BrainF*ck interpreter)
-- Copyright (C) 2020 Brno University of Technology,
--                    Faculty of Information Technology
-- Author(s): Jakub Duda
--

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;

-- ----------------------------------------------------------------------------
--                        Entity declaration
-- ----------------------------------------------------------------------------
entity cpu is
 port (
   CLK   : in std_logic;  -- hodinovy signal
   RESET : in std_logic;  -- asynchronni reset procesoru
   EN    : in std_logic;  -- povoleni cinnosti procesoru
 
   -- synchronni pamet ROM
   CODE_ADDR : out std_logic_vector(11 downto 0); -- adresa do pameti
   CODE_DATA : in std_logic_vector(7 downto 0);   -- CODE_DATA <- rom[CODE_ADDR] pokud CODE_EN='1'
   CODE_EN   : out std_logic;                     -- povoleni cinnosti
   
   -- synchronni pamet RAM
   DATA_ADDR  : out std_logic_vector(9 downto 0); -- adresa do pameti
   DATA_WDATA : out std_logic_vector(7 downto 0); -- ram[DATA_ADDR] <- DATA_WDATA pokud DATA_EN='1'
   DATA_RDATA : in std_logic_vector(7 downto 0);  -- DATA_RDATA <- ram[DATA_ADDR] pokud DATA_EN='1'
   DATA_WE    : out std_logic;                    -- cteni (0) / zapis (1)
   DATA_EN    : out std_logic;                    -- povoleni cinnosti 
   
   -- vstupni port
   IN_DATA   : in std_logic_vector(7 downto 0);   -- IN_DATA <- stav klavesnice pokud IN_VLD='1' a IN_REQ='1'
   IN_VLD    : in std_logic;                      -- data platna
   IN_REQ    : out std_logic;                     -- pozadavek na vstup data
   
   -- vystupni port
   OUT_DATA : out  std_logic_vector(7 downto 0);  -- zapisovana data
   OUT_BUSY : in std_logic;                       -- LCD je zaneprazdnen (1), nelze zapisovat
   OUT_WE   : out std_logic                       -- LCD <- OUT_DATA pokud OUT_WE='1' a OUT_BUSY='0'
 );
end cpu;


-- ----------------------------------------------------------------------------
--                      Architecture declaration
-- ----------------------------------------------------------------------------
architecture behavioral of cpu is

 -- pc 
	signal pc_reg : std_logic_vector(11 downto 0) := (others => '0'); -- pc output
	signal pc_inc : std_logic := '0';							  -- pc increment
	signal pc_dec : std_logic := '0';							  -- pc decrement
	signal pc_ld  : std_logic := '0';							  -- pc load
 -- pc

 -- ras 
	signal ras_reg : std_logic_vector(191 downto 0) := (others => '0'); -- shift register
	signal ras_out : std_logic_vector(11 downto 0) := (others => '0');  -- ras output
	signal ras_push : std_logic := '0'; 							 						  -- rash push
	signal ras_pop  : std_logic := '0'; 							 						  -- ras pop
	signal ras_top  : std_logic := '0'; 							 						  -- ras top
 -- ras

 -- cnt 
	signal cnt_out : std_logic_vector(7 downto 0) := (others => '0'); -- cnt output
	signal cnt_inc : std_logic := '0';  						  -- cnt increment
	signal cnt_dec : std_logic := '0';						  -- cnt decrement
	signal cnt_set : std_logic := '0';						  -- cnt set to '1'
 -- cnt

 -- ptr 
	signal ptr_reg : std_logic_vector(9 downto 0) := (others => '0'); -- ptr output
	signal ptr_inc : std_logic := '0';				 		  -- ptr increment
	signal ptr_dec : std_logic := '0';						  -- ptr decrement
 -- ptr

 -- mux
	signal mux_sel : std_logic_vector(1 downto 0) := (others => '0'); -- mux select
	signal mux_out : std_logic_vector(7 downto 0) := (others => '0'); -- mux output
 -- mux
 
 -- states
	type fsm_state is (s_start, s_fetch, s_decode, s_ptr_inc, s_ptr_dec, 
		s_val_inc, s_val_inc2, s_val_inc3, s_val_dec, s_val_dec2, s_val_dec3, 
		s_while_start, s_while_start2, s_while_skip1, s_while_skip2, s_while_skip3, s_while_end, 
		s_while_end2, s_while_end3, s_get, s_get2, s_get3, s_put, s_put2, s_halt);
	signal p_state : fsm_state := s_start;
	signal n_state : fsm_state := s_start;
	-- states


begin

 -- zde dopiste vlastni VHDL kod


 -- pri tvorbe kodu reflektujte rady ze cviceni INP, zejmena mejte na pameti, ze 
 --   - nelze z vice procesu ovladat stejny signal,
 --   - je vhodne mit jeden proces pro popis jedne hardwarove komponenty, protoze pak
 --   - u synchronnich komponent obsahuje sensitivity list pouze CLK a RESET a 
 --   - u kombinacnich komponent obsahuje sensitivity list vsechny ctene signaly.
 
	
	pc: process(CLK, RESET, pc_inc, pc_dec, pc_ld, ras_reg) is 
	begin
		if RESET = '1' then
			pc_reg <= (others => '0');
		elsif rising_edge(CLK) then
			if pc_inc = '1' then
				pc_reg <= pc_reg + 1;
			elsif pc_dec = '1' then
				pc_reg <= pc_reg - 1;
			elsif pc_ld = '1' then
				pc_reg <= ras_out;
			end if;			
		end if;
	end process;
	CODE_ADDR <= pc_reg;	
	
	ras: process(CLK, RESET, ras_push, ras_pop, ras_top, pc_reg) is
	begin
		if RESET = '1' then
			ras_reg <= (others => '0');
		elsif rising_edge(CLK) then
			if ras_push = '1' then
				ras_reg <= ras_reg(179 downto 0) & (pc_reg + 1);
			elsif ras_pop = '1' then
				ras_out <= ras_reg(11 downto 0);
				ras_reg <= "000000000000" & ras_reg(191 downto 12);
			elsif ras_top = '1' then
				ras_out <= ras_reg(11 downto 0);
			end if;
		end if;
	end process;
	
	cnt: process(CLK, RESET, cnt_inc, cnt_dec, cnt_set) is
	begin
		if RESET = '1' then
			cnt_out <= (others => '0');
		elsif rising_edge(CLK) then
			if cnt_inc = '1' then
				cnt_out <= cnt_out + 1;
			elsif cnt_dec = '1' then
				cnt_out <= cnt_out - 1;
			elsif cnt_set = '1' then
				cnt_out <= "00000001";
			end if;			
		end if;
	end process;
	
	ptr: process(CLK, RESET, ptr_inc, ptr_dec) is 
	begin
		if RESET = '1' then
			ptr_reg <= (others => '0');
		elsif rising_edge(CLK) then
			if ptr_inc = '1' then
				ptr_reg <= ptr_reg + 1;
			elsif ptr_dec = '1' then
				ptr_reg <= ptr_reg - 1;
			end if;
		end if;
	end process;
	DATA_ADDR <= ptr_reg;
	
	mux: process(CLK, RESET, mux_sel) is 
	begin
		if RESET = '1' then
			mux_out <= (others => '0');
		elsif rising_edge(CLK) then
			case mux_sel is
				when "11" => 
					mux_out <= IN_DATA;
				when "10" => 
					mux_out <= DATA_RDATA + 1;
				when "01" => 
					mux_out <= DATA_RDATA - 1;
				when others =>
					mux_out <= (others => '0');
			end case;
		end if;
	end process;
	DATA_WDATA <= mux_out;
	
	fsm_p_state: process(CLK, RESET, EN) is
	begin
		if RESET = '1' then
			p_state <= s_start;
		elsif rising_edge(CLK) then
			if EN = '1' then	
				p_state <= n_state;
			end if;
		end if;
	end process;
	
	fsm_n_state: process(p_state, IN_VLD, OUT_BUSY, CODE_DATA, DATA_RDATA, cnt_out) is
	begin
		-- initialization
		pc_inc <= '0';
		pc_dec <= '0';
		pc_ld <= '0';
		
		ptr_inc <= '0';
		ptr_dec <= '0';
		
		ras_push	<= '0';
		ras_pop <= '0';
		ras_top <= '0';
		
		cnt_set <= '0';
		cnt_inc <= '0';
		cnt_dec <= '0';
		
		mux_sel <= "00";
		
		CODE_EN <= '0';
		IN_REQ <= '0';
		OUT_WE <= '0';
		DATA_WE <= '0';
		DATA_EN <= '0';
		
		-- fsm
		case p_state is
			when s_start =>
				n_state <= s_fetch;
			
			when s_fetch =>
				CODE_EN <= '1';
				n_state <= s_decode;
			
			when s_decode =>
				case CODE_DATA is
					when X"3E" =>
						n_state <= s_ptr_inc;
					when X"3C" =>
						n_state <= s_ptr_dec;
					when X"2B" =>
						n_state <= s_val_inc;
					when X"2D" =>
						n_state <= s_val_dec;
					when X"5B" =>
						n_state <= s_while_start;
					when X"5D" =>
						n_state <= s_while_end;
					when X"2C" =>
						n_state <= s_get;
					when X"2E" =>
						n_state <= s_put;
					when X"00" =>
						n_state <= s_halt;
					when others =>
						pc_inc <= '1';
						n_state <= s_fetch;
				end case;
			
			when s_ptr_inc =>
				ptr_inc <= '1';
				pc_inc <= '1';
				n_state <= s_fetch;
			
			when s_ptr_dec =>
				ptr_dec <= '1';
				pc_inc <= '1';
				n_state <= s_fetch;
			
			when s_val_inc =>
				DATA_EN <= '1';
				DATA_WE <= '0';
				n_state <= s_val_inc2;
			when s_val_inc2 =>
				mux_sel <= "10";
				n_state <= s_val_inc3;
			when s_val_inc3 =>
				DATA_EN <= '1';
				DATA_WE <= '1';
				pc_inc <= '1';
				n_state <= s_fetch;
				
			when s_val_dec =>
				DATA_EN <= '1';
				DATA_WE <= '0';
				n_state <= s_val_dec2;
			when s_val_dec2 =>
				mux_sel <= "01";
				n_state <= s_val_dec3;
			when s_val_dec3 =>
				DATA_EN <= '1';
				DATA_WE <= '1';
				pc_inc <= '1';
				n_state <= s_fetch;
				
			when s_while_start =>
				DATA_EN <= '1';
				DATA_WE <= '0';
				n_state <= s_while_start2;
			when s_while_start2 =>
				if DATA_RDATA = "0000000000" then
					cnt_set <= '1';
					pc_inc <= '1';
					n_state <= s_while_skip1;
				else
					pc_inc <= '1';
					ras_push <= '1';
					n_state <= s_fetch;
				end if;
			when s_while_skip1 =>
				if cnt_out = "00000000" then
					n_state <= s_fetch;
				else
					DATA_EN <= '1';
					DATA_WE <= '0';
					n_state <= s_while_skip2;
				end if;
			when s_while_skip2 =>
				CODE_EN <= '1';
				n_state <= s_while_skip3;
			when s_while_skip3 =>
				if CODE_DATA = X"5B" then
					cnt_inc <= '1';
				elsif CODE_DATA = X"5D" then
					cnt_dec <= '1';
				end if;
				pc_inc <= '1';
				n_state <= s_while_skip1;
				
			when s_while_end =>
				DATA_EN <= '1';
				DATA_WE <= '0';
				n_state <= s_while_end2;
			when s_while_end2 =>
				if DATA_RDATA = "0000000000" then
					ras_pop <= '1';
					pc_inc <= '1';
					n_state <= s_fetch;
				else
					ras_top <= '1';
					n_state <= s_while_end3;
				end if;
			when s_while_end3 =>
				pc_ld <= '1';
				n_state <= s_fetch;

			when s_get =>
				IN_REQ <= '1';
				n_state <= s_get2;
			when s_get2 =>
				if IN_VLD = '0' then
					n_state <= s_get2;
				else
					mux_sel <= "00";
					n_state <= s_get3;
				end if;
			when s_get3 =>
				DATA_EN <= '1';
				DATA_WE <= '1';
				pc_inc <= '1';
				n_state <= s_fetch;
			
			when s_put =>
				if OUT_BUSY = '1' then
					n_state <= s_put;
				else
					DATA_EN <= '1';
					DATA_WE <= '0';
					n_state <= s_put2;
				end if;
			when s_put2 =>
				OUT_DATA <= DATA_RDATA;
				OUT_WE <= '1';
				pc_inc <= '1';
				n_state <= s_fetch;
				
			when s_halt =>
				null;
				
			when others =>
				null;
		end case;
	end process;
	
 
end behavioral;
 



