import { Button, Divider, List } from "antd"
import { useEffect, useState } from "react"
import { UrlUtility } from "../../lib/utilities"
import { Log, LogsData } from "../../lib/types"
import { Search } from "../search"
import { useSearchParams } from "react-router-dom"

interface Props {
  errorMessage: ( message: string ) => void
  successMessage: ( message: string ) => void
}

export const Logs = ( {
  errorMessage,
  successMessage
}: Props ) => {

  const [ searchParams ] = useSearchParams()

  const [ loading, setLoading ] = useState<boolean>( false )
  const [ logs, setLogs ] = useState<Array<Log>>( [] )

  const fetchLogs = async () => {
    setLoading( true )
    const searchCriteria: string | null = searchParams.get( "search" )
    const requestUrl: string = searchCriteria !== null && searchCriteria !== ""
      ? UrlUtility.getSearchLogsUrl( searchCriteria )
      : UrlUtility.getLogsUrl()
    const response = await fetch( requestUrl )
    const logsData: LogsData = await response.json();
    setLogs( logsData.logs )
    setLoading( false )
  }

  const fetchArchiveLogs = async () => {
    if ( logs.length > 0 ) {
      setLoading( true )
      const response = await fetch( UrlUtility.getArchiveLogsUrl( logs[ logs.length - 1 ].id ) )
      const archiveLogsData: LogsData = await response.json()
      if ( archiveLogsData.logs.length > 0 ) {
        successMessage( `${ archiveLogsData.logs.length } logs fetched` )
      } else {
        errorMessage( "No older logs available" )
      }
      setLogs( logs => logs.concat( archiveLogsData.logs ) )
      setLoading( false )
    } else {
      fetchLogs()
    }
  }

  const fetchTailLogs = async () => {
    if ( logs.length > 0 ) {
      setLoading( true )
      const response = await fetch( UrlUtility.getTailLogsUrl( logs[ 0 ].id ) )
      const tailLogsData: LogsData = await response.json()
      if ( tailLogsData.logs.length > 0 ) {
        successMessage( `${ tailLogsData.logs.length } logs fetched` )
      } else {
        errorMessage( "No newer logs available" )
      }
      setLogs( logs => tailLogsData.logs.concat( logs ) )
      setLoading( false )
    } else {
      fetchLogs()
    }
  }

  useEffect( () => {
    fetchLogs()
  }, [ searchParams ] )

  return (
    <>
      <Divider orientation="left">Processor logs</Divider>
      <Search paginationEnabled={ false } searchParams={ searchParams } />
      <List
        size="large"
        bordered
        dataSource={ logs }
        footer={ (
          <div className="text-center">
            <Button
              disabled={ loading }
              loading={ loading }
              onClick={ fetchArchiveLogs }>
              { loading === true && "Loading ..." }
              { loading === false && "Load older logs" }
            </Button>
          </div>
        ) }
        header={ (
          <div className="text-center">
            <Button
              disabled={ loading }
              loading={ loading }
              onClick={ fetchTailLogs }>
              { loading === true && "Loading ..." }
              { loading === false && "Load newer logs" }
            </Button>
          </div>
        ) }
        renderItem={ ( log: Log ) => (
          <List.Item>
            [{ log.created }] { log.text }
          </List.Item>
        ) }
      />
    </>
  )
}