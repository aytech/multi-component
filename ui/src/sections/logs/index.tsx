import { Divider, List } from "antd"
import { useEffect, useState } from "react"
import { UrlUtility } from "../../lib/utilities"
import { LogsData } from "../../lib/types"

export const Logs = () => {

  const [ loading, setLoading ] = useState<boolean>( false )
  const [ lastLogId, setLastLogId ] = useState<number>( 1 )
  const [ logsData, setLogsData ] = useState<LogsData | null>( null )

  const fetchLogs = async () => {
    setLoading( true )
    const response = await fetch( UrlUtility.getLogsUrl( lastLogId, 100 ) )
    const logsData: LogsData = await response.json();
    setLogsData( logsData )
    setLoading( false )
  }

  useEffect( () => {
    fetchLogs()
  } )

  return (
    <>
      <Divider orientation="left">Processor logs</Divider>
      <List
        size="large"
        bordered
        dataSource={ logsData?.logs }
        renderItem={ ( item ) => <List.Item>{ item }</List.Item> }
      />
    </>
  )
}