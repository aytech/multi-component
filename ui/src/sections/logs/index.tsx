import { Button, Divider, List } from "antd"
import { useEffect, useState } from "react"
import { UrlUtility } from "../../lib/utilities"
import { Log, LogsData } from "../../lib/types"
import { LoadingOutlined } from "@ant-design/icons"
import "./styles.css"

export const Logs = () => {

  const [ loading, setLoading ] = useState<boolean>( false )
  const [ lastLogId, setLastLogId ] = useState<number | null>( null )
  const [ logsData, setLogsData ] = useState<LogsData | null>( null )
  const [ logsFetchInterval, setLogsFetchInterval ] = useState<NodeJS.Timer>()

  const fetchLogs = async () => {
    setLoading( true )
    const response = await fetch( UrlUtility.getLogsUrl( 100, lastLogId ) )
    const logsData: LogsData = await response.json();
    setLogsData( logsData )
    setLoading( false )
  }

  const Header = () => loading ? (
    <div className="text-center logs-header">
      <em>Loading newer logs...</em> <LoadingOutlined />
    </div>
  ) : null

  useEffect( () => {
    fetchLogs()
    setLogsFetchInterval( setInterval( () => {
      setLoading( true )
      console.log( "Fetching newer logs" )
      setTimeout( () => setLoading( false ), 3000 )
    }, 8000 ) )
    return () => clearInterval( logsFetchInterval )
  }, [] )

  return (
    <>
      <Divider orientation="left">Processor logs</Divider>
      <List
        size="large"
        bordered
        dataSource={ logsData?.logs }
        footer={ (
          <div className="text-center">
            <Button
              disabled={ loading }
              loading={ loading }
              onClick={ () => {
                setLoading( true )
                setTimeout( () => setLoading( false ), 3000 )
              } }>
              { loading === true && "Loading ..." }
              { loading === false && "Load older logs" }
            </Button>
          </div>
        ) }
        header={ <Header /> }
        renderItem={ ( log: Log ) => (
          <List.Item>
            [{ log.created }] { log.text }
          </List.Item>
        ) }
      />
    </>
  )
}