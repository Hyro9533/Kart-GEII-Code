#ifndef __MODULE_LORA_H__
#define __MODULE_LORA_H__

///////////////////////////////////////////////////////////////////////////////
// Module LoRa handler class
///////////////////////////////////////////////////////////////////////////////
class CModuleLoRa
{
public:
  static CModuleLoRa* GetInstance();
  
  CModuleLoRa(CModuleLoRa &other) = delete;        // Singletons should not be cloneable
  void operator=(const CModuleLoRa &) = delete;    // Singletons should not be assignable

  void init(const uint8_t pinHWReset, const uint8_t pinRX, const uint8_t pinTX);
  bool hwReset();
  bool reset();
  bool resetFactory();
  bool getInfo();
  bool getConfig();
  bool setConfig();
  bool radioTX(const uint8_t* pData, uint16_t len);
  bool radioRX(String& rxData, long int nTimeout);

private:
  bool send_data(const char* pszData);
  bool rcv_data(long int nTimeout, String& rcvLine);
  bool send_cmd(String cmd, String& rsp, String expectedRsp="");

private:
  uint8_t m_pinHWReset;
  HardwareSerial* pSerialPort;
   
protected:
  CModuleLoRa();
  static CModuleLoRa* _singleton;
};

#endif // __MODULE_LORA_H__