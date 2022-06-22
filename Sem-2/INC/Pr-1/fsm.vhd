-- fsm.vhd: Finite State Machine
-- Author(s): Jakub Duda
--
library ieee;
use ieee.std_logic_1164.all;
-- ----------------------------------------------------------------------------
--                        Entity declaration
-- ----------------------------------------------------------------------------
entity fsm is
port(
   CLK         : in  std_logic;
   RESET       : in  std_logic;

   -- Input signals
   KEY         : in  std_logic_vector(15 downto 0);
   CNT_OF      : in  std_logic;

   -- Output signals
   FSM_CNT_CE  : out std_logic;
   FSM_MX_MEM  : out std_logic;
   FSM_MX_LCD  : out std_logic;
   FSM_LCD_WR  : out std_logic;
   FSM_LCD_CLR : out std_logic
);
end entity fsm;

-- xdudaj02 :
-- kod1 = 956335091 	
-- kod2 = 9562513184	

-- ----------------------------------------------------------------------------
--                      Architecture declaration
-- ----------------------------------------------------------------------------
architecture behavioral of fsm is
   type t_state is (STATE_DEFAULT, STATE_VALID, STATE_INVALID, TEST_AB01, TEST_AB02, TEST_AB03, TEST_A04, TEST_A05, TEST_A06, TEST_A07, TEST_A08, TEST_B04, TEST_B05, TEST_B06, TEST_B07, TEST_B08, TEST_B09, PRINT_VALID, PRINT_INVALID, FINISH);
   signal present_state, next_state : t_state;

begin
-- -------------------------------------------------------
sync_logic : process(RESET, CLK)
begin
   if (RESET = '1') then
      present_state <= STATE_DEFAULT;
   elsif (CLK'event AND CLK = '1') then
      present_state <= next_state;
   end if;
end process sync_logic;

-- -------------------------------------------------------
next_state_logic : process(present_state, KEY, CNT_OF)
begin
   case (present_state) is
   -- - - - - - - - - - - - - - - - - - - - - - -
   when STATE_DEFAULT =>
      next_state <= STATE_DEFAULT;
		if (KEY(15) = '1') then
         next_state <= PRINT_INVALID; 
		elsif (KEY(9) = '1') then
			next_state <= TEST_AB01; 
		elsif (KEY(14 downto 0) /= "000000000000000") then	
			next_state <= STATE_INVALID;
      end if;
	-- - - - - - - - - - - - - - - - - - - - - - -
   when TEST_AB01 =>
      next_state <= TEST_AB01;
		if (KEY(15) = '1') then
			next_state <= PRINT_INVALID;
      elsif (KEY(5) = '1') then
         next_state <= TEST_AB02; 
		elsif (KEY(14 downto 0) /= "000000000000000") then	
			next_state <= STATE_INVALID;
      end if;
	-- - - - - - - - - - - - - - - - - - - - - - -
   when TEST_AB02 =>
      next_state <= TEST_AB02;
		if (KEY(15) = '1') then
			next_state <= PRINT_INVALID;
      elsif (KEY(6) = '1') then
         next_state <= TEST_AB03; 
		elsif (KEY(14 downto 0) /= "000000000000000") then	
			next_state <= STATE_INVALID;
      end if;
	-- - - - - - - - - - - - - - - - - - - - - - -
   when TEST_AB03 =>
      next_state <= TEST_AB03;
		if (KEY(15) = '1') then
			next_state <= PRINT_INVALID;
      elsif (KEY(3) = '1') then
         next_state <= TEST_A04; 
		elsif (KEY(2) = '1') then
         next_state <= TEST_B04;
		elsif (KEY(14 downto 0) /= "000000000000000") then	
			next_state <= STATE_INVALID;
      end if;
	-- - - - - - - - - - - - - - - - - - - - - - -
   when TEST_A04 =>
      next_state <= TEST_A04;
		if (KEY(15) = '1') then
			next_state <= PRINT_INVALID;
      elsif (KEY(3) = '1') then
         next_state <= TEST_A05;
		elsif (KEY(14 downto 0) /= "000000000000000") then	
			next_state <= STATE_INVALID;
      end if;
	-- - - - - - - - - - - - - - - - - - - - - - -
   when TEST_B04 =>
      next_state <= TEST_B04;
		if (KEY(15) = '1') then
			next_state <= PRINT_INVALID;
      elsif (KEY(5) = '1') then
         next_state <= TEST_B05;
		elsif (KEY(14 downto 0) /= "000000000000000") then	
			next_state <= STATE_INVALID;
      end if;
   -- - - - - - - - - - - - - - - - - - - - - - -
   when TEST_A05 =>
      next_state <= TEST_A05;
		if (KEY(15) = '1') then
			next_state <= PRINT_INVALID;
      elsif (KEY(5) = '1') then
         next_state <= TEST_A06;
		elsif (KEY(14 downto 0) /= "000000000000000") then	
			next_state <= STATE_INVALID;
      end if;
	-- - - - - - - - - - - - - - - - - - - - - - -
   when TEST_B05 =>
      next_state <= TEST_B05;
		if (KEY(15) = '1') then
			next_state <= PRINT_INVALID;
      elsif (KEY(1) = '1') then
         next_state <= TEST_B06;
		elsif (KEY(14 downto 0) /= "000000000000000") then	
			next_state <= STATE_INVALID;
      end if;
	-- - - - - - - - - - - - - - - - - - - - - - -
   when TEST_A06 =>
      next_state <= TEST_A06;
		if (KEY(15) = '1') then
			next_state <= PRINT_INVALID;
      elsif (KEY(0) = '1') then
         next_state <= TEST_A07;
		elsif (KEY(14 downto 0) /= "000000000000000") then	
			next_state <= STATE_INVALID;
      end if;
	-- - - - - - - - - - - - - - - - - - - - - - -
   when TEST_B06 =>
      next_state <= TEST_B06;
		if (KEY(15) = '1') then
			next_state <= PRINT_INVALID;
      elsif (KEY(3) = '1') then
         next_state <= TEST_B07;
		elsif (KEY(14 downto 0) /= "000000000000000") then	
			next_state <= STATE_INVALID;
      end if;
	-- - - - - - - - - - - - - - - - - - - - - - -
   when TEST_A07 =>
      next_state <= TEST_A07;
		if (KEY(15) = '1') then
			next_state <= PRINT_INVALID;
      elsif (KEY(9) = '1') then
         next_state <= TEST_A08;
		elsif (KEY(14 downto 0) /= "000000000000000") then	
			next_state <= STATE_INVALID;
      end if;
	-- - - - - - - - - - - - - - - - - - - - - - -
   when TEST_B07 =>
      next_state <= TEST_B07;
		if (KEY(15) = '1') then
			next_state <= PRINT_INVALID;
      elsif (KEY(1) = '1') then
         next_state <= TEST_B08;
		elsif (KEY(14 downto 0) /= "000000000000000") then	
			next_state <= STATE_INVALID;
      end if;
	-- - - - - - - - - - - - - - - - - - - - - - -
   when TEST_A08 =>
      next_state <= TEST_A08;
		if (KEY(15) = '1') then
			next_state <= PRINT_INVALID;
      elsif (KEY(1) = '1') then
         next_state <= STATE_VALID;
		elsif (KEY(14 downto 0) /= "000000000000000") then	
			next_state <= STATE_INVALID;
      end if;
	-- - - - - - - - - - - - - - - - - - - - - - -
   when TEST_B08 =>
      next_state <= TEST_B08;
		if (KEY(15) = '1') then
			next_state <= PRINT_INVALID;
      elsif (KEY(8) = '1') then
         next_state <= TEST_B09;
		elsif (KEY(14 downto 0) /= "000000000000000") then	
			next_state <= STATE_INVALID;
      end if;	
	-- - - - - - - - - - - - - - - - - - - - - - -
   when TEST_B09 =>
      next_state <= TEST_B09;
		if (KEY(15) = '1') then
			next_state <= PRINT_INVALID;
      elsif (KEY(4) = '1') then
         next_state <= STATE_VALID;
		elsif (KEY(14 downto 0) /= "000000000000000") then	
			next_state <= STATE_INVALID;
      end if;
	-- - - - - - - - - - - - - - - - - - - - - - -
	when STATE_VALID =>
		next_state <= STATE_VALID;
		if (KEY(15) = '1') then
			next_state <= PRINT_VALID;
		elsif (KEY(14 downto 0) /= "000000000000000") then	
			next_state <= STATE_INVALID;
		end if;
	-- - - - - - - - - - - - - - - - - - - - - - -
	when STATE_INVALID =>
		next_state <= STATE_INVALID;
		if (KEY(15) = '1') then
			next_state <= PRINT_INVALID;
		end if;
	-- - - - - - - - - - - - - - - - - - - - - - -
	when PRINT_VALID =>
		next_state <= PRINT_VALID;
		if (CNT_OF = '1') then
			next_state <= FINISH;
		end if;
	-- - - - - - - - - - - - - - - - - - - - - - -
	when PRINT_INVALID =>
		next_state <= PRINT_INVALID;
		if (CNT_OF = '1') then
			next_state <= FINISH;
		end if;
   -- - - - - - - - - - - - - - - - - - - - - - -
   when FINISH =>
      next_state <= FINISH;
      if (KEY(15) = '1') then
         next_state <= STATE_DEFAULT; 
      end if;
   -- - - - - - - - - - - - - - - - - - - - - - -
   when others =>
		null;
   end case;
end process next_state_logic;

-- -------------------------------------------------------
output_logic : process(present_state, KEY)
begin
   FSM_CNT_CE     <= '0';
   FSM_MX_MEM     <= '0';
   FSM_MX_LCD     <= '0';
   FSM_LCD_WR     <= '0';
   FSM_LCD_CLR    <= '0';

   case (present_state) is
   -- - - - - - - - - - - - - - - - - - - - - - -
   when STATE_DEFAULT | STATE_VALID | STATE_INVALID | TEST_AB01 | TEST_AB02 | TEST_AB03 | TEST_A04 | TEST_A05 | TEST_A06 | TEST_A07 | TEST_A08 | TEST_B04 | TEST_B05 | TEST_B06 | TEST_B07  | TEST_B08 | TEST_B09 =>
      if (KEY(14 downto 0) /= "000000000000000") then
         FSM_LCD_WR     <= '1';
      end if;
      if (KEY(15) = '1') then
         FSM_LCD_CLR    <= '1';
      end if;
   -- - - - - - - - - - - - - - - - - - - - - - -
   when PRINT_VALID =>
      FSM_CNT_CE     <= '1';
		FSM_MX_MEM     <= '1';
		FSM_MX_LCD     <= '1';
      FSM_LCD_WR     <= '1';
   -- - - - - - - - - - - - - - - - - - - - - - -
   when PRINT_INVALID =>
      FSM_CNT_CE     <= '1';
      FSM_MX_LCD     <= '1';
      FSM_LCD_WR     <= '1';
   -- - - - - - - - - - - - - - - - - - - - - - -
   when FINISH =>
      if (KEY(15) = '1') then
         FSM_LCD_CLR    <= '1';
      end if;
   -- - - - - - - - - - - - - - - - - - - - - - -
   end case;
end process output_logic;

end architecture behavioral;
