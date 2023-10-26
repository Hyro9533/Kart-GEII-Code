#include "module_lora.h"

#define RN2483_TIMEOUT              1000
#define RN2483_BAUDRATE             57600

#define RN2483_CMD_ENDING           "\r\n"
#define RN2483_RSP_OK               "ok"
#define RN2483_RSP_TX_OK            "radio_tx_ok"
#define RN2483_RSP_RX_OK            "radio_rx  "
#define RN2483_RSP_MAC_PAUSE_OK     "4294967245"  // 0xFFFFFFCD
#define RN2483_RSP_RESET            "RN2483"

// Mac commands
#define RN2483_CMD_PAUSE_MAC        "mac pause"

// Sys commands
#define RN2483_CMD_RESET            "sys reset"
#define RN2483_CMD_FACTORY_RESET    "sys factoryRESET"
#define RN2483_CMD_GET_VERSION      "sys get ver"
#define RN2483_CMD_GET_HWEUI        "sys get hweui"
#define RN2483_CMD_GET_VOLTAGE      "sys get vdd"

// Radio commands
#define RN2483_CMD_TX               "radio tx"
#define RN2483_CMD_RX               "radio rx"

// Radio parameters
#define RN2483_CMD_GET_MODE         "radio get mod"
#define RN2483_CMD_GET_FREQUENCY    "radio get freq"
#define RN2483_CMD_GET_POWER        "radio get pwr"
#define RN2483_CMD_GET_SF           "radio get sf"
#define RN2483_CMD_GET_RX_BW        "radio get rxbw"
#define RN2483_CMD_GET_PR_LEN       "radio get prlen"
#define RN2483_CMD_GET_CRC          "radio get crc"
#define RN2483_CMD_GET_IQI          "radio get iqi"
#define RN2483_CMD_GET_CODING_RATE  "radio get cr"
#define RN2483_CMD_GET_WDT          "radio get wdt"
#define RN2483_CMD_GET_SYNC         "radio get sync"
#define RN2483_CMD_GET_BW           "radio get bw"

#define RN2483_CMD_SET_MODE         "radio set mod lora"
#define RN2483_CMD_SET_FREQUENCY    "radio set freq 868100000"
#define RN2483_CMD_SET_POWER        "radio set pwr 15"
#define RN2483_CMD_SET_SF           "radio set sf sf12"
#define RN2483_CMD_SET_RX_BW        "radio set rxbw 125"
#define RN2483_CMD_SET_PR_LEN       "radio set prlen 8"
#define RN2483_CMD_SET_CRC          "radio set crc on"
#define RN2483_CMD_SET_IQI          "radio set iqi off"
#define RN2483_CMD_SET_CODING_RATE  "radio set cr 4/5"
#define RN2483_CMD_SET_WDT          "radio set wdt 0"         // 0 for continous reception, otherwise 2000 
#define RN2483_CMD_SET_SYNC         "radio set sync 12"       // 34 public, 12 private network
#define RN2483_CMD_SET_BW           "radio set bw 125"

CModuleLoRa* CModuleLoRa::_singleton = nullptr;

///////////////////////////////////////////////////////////////////////////////
CModuleLoRa::CModuleLoRa()
{
  m_pinHWReset = 0;

  pSerialPort = new HardwareSerial(1);
}

///////////////////////////////////////////////////////////////////////////////
CModuleLoRa* CModuleLoRa::GetInstance()
{
  if( _singleton == nullptr )
    _singleton = new CModuleLoRa();

  return _singleton;
}

///////////////////////////////////////////////////////////////////////////////
void CModuleLoRa::init(const uint8_t pinHWReset, const uint8_t pinRX, const uint8_t pinTX)
{
  m_pinHWReset = pinHWReset;

  pinMode(m_pinHWReset, OUTPUT);
  digitalWrite(m_pinHWReset, HIGH);

  pSerialPort->begin(RN2483_BAUDRATE, SERIAL_8N1, pinRX, pinTX);
}

///////////////////////////////////////////////////////////////////////////////
bool CModuleLoRa::hwReset()
{
  Serial.println("[RN2483] Hardware reset...");

  digitalWrite(m_pinHWReset, LOW);
  delay(10);
  digitalWrite(m_pinHWReset, HIGH);

  String rsp;
  if( rcv_data(RN2483_TIMEOUT, rsp) && rsp.startsWith(RN2483_RSP_RESET) )
  {
    rcv_data(RN2483_TIMEOUT, rsp); // Read extra data comming in
    
    Serial.println("[RN2483] Hardware detected.");
    return true;
  }

  return false;
}

///////////////////////////////////////////////////////////////////////////////
bool CModuleLoRa::reset()
{
  String rsp;
  if( send_cmd(RN2483_CMD_RESET, rsp, RN2483_RSP_RESET) )
  {
    Serial.println("[RN2483] Hardware detected.");
    return true;
  }

  return false;
}

///////////////////////////////////////////////////////////////////////////////
bool CModuleLoRa::resetFactory()
{
  String rsp;
  if( send_cmd(RN2483_CMD_FACTORY_RESET, rsp, RN2483_RSP_RESET) )
  {
    Serial.println("[RN2483] Hardware detected.");
    return true;
  }

  return false;
}

///////////////////////////////////////////////////////////////////////////////
bool CModuleLoRa::send_data(const char* pszData)
{
  Serial.print("[RN2483] >> ");
  Serial.print(pszData);
  return (pSerialPort->write(pszData) == strlen(pszData));
}

///////////////////////////////////////////////////////////////////////////////
bool CModuleLoRa::rcv_data(long int nTimeout, String& rcvLine)
{
  rcvLine = "";

  long int nElapsedTime = millis();
  
  while( millis() - nElapsedTime < nTimeout )
  {
    while( pSerialPort->available() ) 
    {
      char c = pSerialPort->read();

      if( c == '\r' || c == '\n' || std::isprint(static_cast<unsigned char>(c)) )
      {
        nElapsedTime = millis();
        
        // End of line ?
        if( c == '\n' )
        {
          // Only return non empty lines
          if( rcvLine.length() > 0 )
          {
            Serial.println("[RN2483] << " + rcvLine);
            return true;
          }
        }
        else
        {
          if( c != '\r' && c != '\n' )
            rcvLine += c;
        }
      }
      else
        break;
    }
  }

  return false;
}

///////////////////////////////////////////////////////////////////////////////
bool CModuleLoRa::send_cmd(String cmd, String& rsp, String expectedRsp/*=""*/)
{
  cmd += RN2483_CMD_ENDING;

  if( !send_data(cmd.c_str()) )
    return false;

  uint8_t t = 0;

  while( ++t < 3 )
  {
    if( rcv_data(RN2483_TIMEOUT, rsp) )
    {
      if( expectedRsp.length() )
      {
        if( rsp.startsWith(expectedRsp) )
          return true;
      }
      else
        return true;
    }
  }

  return false;
}

///////////////////////////////////////////////////////////////////////////////
bool CModuleLoRa::getInfo()
{
  String rsp;
  if( !send_cmd(RN2483_CMD_GET_VERSION, rsp) )
    return false;

  if( !send_cmd(RN2483_CMD_GET_HWEUI, rsp) )
    return false;

  if( !send_cmd(RN2483_CMD_GET_VOLTAGE, rsp) )
    return false;

  return true;
}

///////////////////////////////////////////////////////////////////////////////
bool CModuleLoRa::getConfig()
{
  String rsp;
  if( !send_cmd(RN2483_CMD_GET_MODE, rsp) )
    return false;

  if( !send_cmd(RN2483_CMD_GET_FREQUENCY, rsp) )
    return false;

  if( !send_cmd(RN2483_CMD_GET_POWER, rsp) )
    return false;

  if( !send_cmd(RN2483_CMD_GET_SF, rsp) )
    return false;

  if( !send_cmd(RN2483_CMD_GET_RX_BW, rsp) )
    return false;

  if( !send_cmd(RN2483_CMD_GET_PR_LEN, rsp) )
    return false;

  if( !send_cmd(RN2483_CMD_GET_CRC, rsp) )
    return false;

  if( !send_cmd(RN2483_CMD_GET_IQI, rsp) )
    return false;

  if( !send_cmd(RN2483_CMD_GET_CODING_RATE, rsp) )
    return false;

  if( !send_cmd(RN2483_CMD_GET_WDT, rsp) )
    return false;

  if( !send_cmd(RN2483_CMD_GET_SYNC, rsp) )
    return false;

  if( !send_cmd(RN2483_CMD_GET_BW, rsp) )
    return false;

  return true;
}

///////////////////////////////////////////////////////////////////////////////
bool CModuleLoRa::setConfig()
{
  String rsp;
  if( !send_cmd(RN2483_CMD_PAUSE_MAC, rsp, RN2483_RSP_MAC_PAUSE_OK) )
    return false;

  if( !send_cmd(RN2483_CMD_SET_MODE, rsp, RN2483_RSP_OK) )
    return false;

  if( !send_cmd(RN2483_CMD_SET_FREQUENCY, rsp, RN2483_RSP_OK) )
    return false;

  if( !send_cmd(RN2483_CMD_SET_POWER, rsp, RN2483_RSP_OK) )
    return false;

  if( !send_cmd(RN2483_CMD_SET_SF, rsp, RN2483_RSP_OK) )
    return false;

  if( !send_cmd(RN2483_CMD_SET_RX_BW, rsp, RN2483_RSP_OK) )
    return false;

  if( !send_cmd(RN2483_CMD_SET_PR_LEN, rsp, RN2483_RSP_OK) )
    return false;

  if( !send_cmd(RN2483_CMD_SET_CRC, rsp, RN2483_RSP_OK) )
    return false;

  if( !send_cmd(RN2483_CMD_SET_IQI, rsp, RN2483_RSP_OK) )
    return false;

  if( !send_cmd(RN2483_CMD_SET_CODING_RATE, rsp, RN2483_RSP_OK) )
    return false;

  if( !send_cmd(RN2483_CMD_SET_WDT, rsp, RN2483_RSP_OK) )
    return false;

  if( !send_cmd(RN2483_CMD_SET_SYNC, rsp, RN2483_RSP_OK) )
    return false;

  if( !send_cmd(RN2483_CMD_SET_BW, rsp, RN2483_RSP_OK) )
    return false;

  return true;
}

///////////////////////////////////////////////////////////////////////////////
bool CModuleLoRa::radioTX(const uint8_t* pData, uint16_t len)
{
  String rsp;
  if( !send_cmd(RN2483_CMD_PAUSE_MAC, rsp, RN2483_RSP_MAC_PAUSE_OK) )
    return false;

  String cmd = RN2483_CMD_TX;
  cmd += " ";

  // Add data (hex)
  char szTmp[3] = {0};
  for(uint16_t i = 0; i < len; i++ )
  {
    sprintf(szTmp, "%02X", *(pData+i));
    cmd += szTmp;
  }

  if( !send_cmd(cmd, rsp, RN2483_RSP_TX_OK) )
    return false;

  return true;
}

///////////////////////////////////////////////////////////////////////////////
bool CModuleLoRa::radioRX(String& rxData, long int nTimeout)
{
  String rsp;
  if( !send_cmd(RN2483_CMD_PAUSE_MAC, rsp, RN2483_RSP_MAC_PAUSE_OK) )
    return false;

  String cmdRX0 = RN2483_CMD_RX;
  cmdRX0 += " 0";

  if( !send_cmd(cmdRX0, rsp, RN2483_RSP_OK) )
    return false;

  long int tInit = millis();

  while( 1 )
  {
    rcv_data(RN2483_TIMEOUT, rxData);

    if( rxData.length() )
    {
      if( !rxData.startsWith(RN2483_RSP_RX_OK) )
      {
        rxData = "";
        return false;
      }

      // Filter response heading
      rxData.replace(RN2483_RSP_RX_OK, "");

      break;
    }
    else if( nTimeout != 0 && millis() > tInit + nTimeout )
    {
      return false;
    }
  }

  return true;
}
