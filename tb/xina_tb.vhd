----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 08/05/2021 
-- Design Name: 
-- Module Name: file_xina_tb - Behavioral
-- Project Name: 
-- Target Devices: 
-- Tool Versions: 
-- Description: 
-- 
-- Dependencies: 
-- 
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
-- 
----------------------------------------------------------------------------------

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use std.textio.all;
use ieee.std_logic_textio.all;


entity xina_tb is
    generic (
    -- # of routers in x and y
    rows_p : positive := 4;
    cols_p : positive := 4;
    -- input and output flow regulation mode
    flow_mode_p : natural := 0; -- 0 for HS Moore, 1 for HS Mealy
    -- routing mode
    routing_mode_p : natural := 0; -- 0 for XY Moore, 1 for XY Mealy
    -- arbitration mode
    arbitration_mode_p : natural := 0; -- 0 for RR Moore, 1 for RR Mealy
    -- input buffer mode and depth
    buffer_mode_p  : natural  := 0; -- 0 for FIFO Ring, 1 for FIFO Shift
    buffer_depth_p : positive := 4;
    -- network data width
    data_width_p : positive := 8
      );
end xina_tb;

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use work.xina_pkg.all;
use std.textio.all;
use ieee.std_logic_textio.all;


architecture Behavioral of xina_tb is

constant n_packets : integer := 10; --number of messages that will be used on the testebench
constant n_flits :  integer := 4; --number of flits that each packet has

constant period_c : time := 10 ns;
signal clk_i        : std_logic := '0';
signal rst_i        : std_logic := '0';
signal l_in_data_i  : data_link_l_t;
signal l_in_val_i   : ctrl_link_l_t;
signal l_in_ack_o   : ctrl_link_l_t;
signal l_out_data_o : data_link_l_t;
signal l_out_val_o  : ctrl_link_l_t;
signal l_out_ack_i  : ctrl_link_l_t;

component xina
generic (
    -- # of routers in x and y
    rows_p : positive := rows_c;
    cols_p : positive := cols_c;
    -- input and output flow regulation mode
    flow_mode_p : natural := flow_mode_c; -- 0 for HS Moore, 1 for HS Mealy
    -- routing mode
    routing_mode_p : natural := routing_mode_c; -- 0 for XY Moore, 1 for XY Mealy
    -- arbitration mode
    arbitration_mode_p : natural := arbitration_mode_c; -- 0 for RR Moore, 1 for RR Mealy
    -- input buffer mode and depth
    buffer_mode_p  : natural  := buffer_mode_c; -- 0 for FIFO Ring, 1 for FIFO Shift
    buffer_depth_p : positive := buffer_depth_c;
    -- network data width
    data_width_p : positive := data_width_c
    );
  port (
    -- control signals
    clk_i        : in  std_logic;
    rst_i        : in  std_logic;
    -- local channel interface
    l_in_data_i  : in  data_link_l_t;
    l_in_val_i   : in  ctrl_link_l_t;
    l_in_ack_o   : out ctrl_link_l_t;
    l_out_data_o : out data_link_l_t;
    l_out_val_o  : out ctrl_link_l_t;
    l_out_ack_i  : in  ctrl_link_l_t
    );
end component;

begin

--noc port map
xina_0000 : xina
    generic map(
      rows_p       => rows_c,
      cols_p       => cols_c,
      flow_mode_p    => flow_mode_p,
      routing_mode_p    => routing_mode_p,
      arbitration_mode_p    => arbitration_mode_p,
      buffer_mode_p  => buffer_mode_p,
      buffer_depth_p => buffer_depth_p,
      data_width_p => data_width_p
      )
    port map (
      clk_i=> clk_i,
      rst_i=> rst_i,
      l_in_data_i=> l_in_data_i,
      l_in_val_i=> l_in_val_i,
      l_in_ack_o=> l_in_ack_o,
      l_out_data_o=> l_out_data_o,
      l_out_val_o=> l_out_val_o,
      l_out_ack_i=> l_out_ack_i
      );

clk_i <= not clk_i after period_c/2;
rst_i <= '1', '0' after period_c;

--Entry generation
col_entry : for x in cols_c-1 downto 0 generate
    row_entry : for y in rows_c-1 downto 0 generate
        process 
            file txt_reader : text open read_mode is ("/home/haas/Documents/github/xina_sim/input_files_tb/tb_input_router_"&integer'image(X)&integer'image(Y)&".txt");--
            variable v_iline : line;
            variable temporary_read_value : std_logic_vector(8 downto 0);
            variable counter : integer := 0;
            begin
                for I in (n_packets*n_flits-1) downto 0 loop   
                    l_in_val_i(X,Y) <= '0';
                    if (counter<n_flits*n_packets) then--reads logs to get input data
                        readline(txt_reader, v_ILINE);
                        read(v_ILINE, temporary_read_value);
                        l_in_data_i(X,Y)<= temporary_read_value;
                        counter:=counter+1; 
                    else
                        l_in_data_i(X,Y)<="000000000";
                    end if;
                    if(flow_mode_p=0) then--If flow mode is Moore it does another wait period
                        wait for period_c;
                    end if;
                    l_in_val_i(X,Y)  <= '1';
                    wait until l_in_ack_o(X,Y) = '1';
                    wait for period_c;
                    l_in_val_i(X,Y)  <= '0';
                    wait until l_in_ack_o(X,Y) = '0';
                end loop;
        end process;
    end generate;
end generate;


--backup Exits generation
col_exit : for x in cols_c-1 downto 0 generate
    row_exit : for y in rows_c-1 downto 0 generate
        process 
            variable v_oline:line;
            variable counter : integer := 0;
            variable v_TIME : time := 0 ns;
            file log_writer : text open write_mode is ("/home/haas/Documents/github/xina_sim/log_tb/tb_router_"&integer'image(X)&integer'image(Y)&".log");
            begin
                l_out_ack_i(X,Y) <= '0';
                wait until l_out_val_o(X,Y) = '1';
                wait for period_c;
                l_out_ack_i(X,Y) <= '1';
                if (counter<n_flits*n_packets) then
                    v_TIME := now;
                    write(v_oline,l_out_data_o(X,Y));
                    write(v_oline,string'(","));
                    write(v_oline,v_TIME);
                    writeline(log_writer,v_oline);
                    counter:=counter+1;
                 end if;
                wait until l_out_val_o(X,Y)='0';
                wait for period_c;
        end process;
    end generate;
end generate;

end Behavioral;

