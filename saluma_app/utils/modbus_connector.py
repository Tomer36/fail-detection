from easymodbus.modbusClient import ModbusClient, convert_registers_to_float


def connection_to_modbus(self):
    select_for_ip_and_port = ("SELECT * FROM setting WHERE id = 1")
    self.cursor.execute(select_for_ip_and_port)
    res_for_ip_and_port = self.cursor.fetchall()
    print('Params for connection from table setting!')
    print(res_for_ip_and_port)
    # mb_ip = self.st.get_setting('MB_IP_ADDRESS')
    # mb_port = self.st.get_setting('MB_PORT')
    mb_ip = res_for_ip_and_port[0]['MB_IP_ADDRESS']
    mb_port = res_for_ip_and_port[0]['MB_PORT']
    print('IP and PORT = {}, {}'.format(mb_ip, mb_port))
    self.modbus_client = ModbusClient(mb_ip, int(mb_port))
    print('~~~~~~~~~~~~~~~~~Mobdus connected~~~~~~~~~~~~~~~~~')
    try:
        self.modbus_client.connect()
    except Exception as err:
        print('!!!!!!!!!!!!!!!!!!!Havent connection to modbus!!!!!!!!!!!!!!!!!!')
        print(err)

    def read_mb_2(self):
        # create modbus prop
        self.set_table(self.CONFIG_TABLE_NAME)
        select = self.select().exe()
        insert = {}

        full_values_for_modbus = self.modbus_client.read_holdingregisters(0, 21)

        for row in select:
            tag_name = row['TAG_NAME']
            mb_type = row['MB_TYPE']
            mb_address = row['MB_ADDRESS']

            # Modbus read function by mb type
            if mb_type == self.COL_TYPE_FLOAT:
                double_value = []
                double_value.append(full_values_for_modbus[0])
                double_value.append(full_values_for_modbus[1])
                full_value = convert_registers_to_float(double_value)
                insert[tag_name] = str(full_value[0])
                del full_values_for_modbus[0]
                del full_values_for_modbus[0]
            elif mb_type == self.COL_TYPE_INT:
                insert[tag_name] = str(full_values_for_modbus[0])
                del full_values_for_modbus[0]
            # elif mb_type == self.COL_TYPE_BOOL:
            #     val = self.modbus_client.read_coils()


            # # Modbus read function by mb type
            # from_address = int(mb_address)
            # if mb_type == self.COL_TYPE_FLOAT:
            #     val = convert_registers_to_float(self.modbus_client.read_holdingregisters(from_address, 2))
            #     insert[tag_name] = str(val[0])
            # elif mb_type == self.COL_TYPE_INT:
            #     val = self.modbus_client.read_holdingregisters(from_address, 1)
            #     insert[tag_name] = str(val[0])


        self.set_table(self.DATA_TABLE_NAME)
        print(insert)
        return self.insert(insert)

connection_to_modbus()
read_mb_2()
modbus_client.close()