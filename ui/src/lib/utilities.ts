import { Page } from "./types"

export const UrlUtility = {
  getUserSearchUrl: ( page: Page ) => {
    let url = `/api/users/search/${page.search}?page=${page.page}&size=${page.size}`
    if ( page.status !== undefined ) {
      url += `&status=${page.status}`
    }
    return url
  },
  getUsersUrl: ( page: Page ) => {
    let url = `/api/users?page=${page.page}&size=${page.size}`
    if ( page.status !== undefined ) {
      url += `&status=${page.status}`
    }
    return url
  },
  getLogsUrl: () => {
    return "/api/logs"
  },
  getArchiveLogsUrl: ( from: number ) => {
    return `${UrlUtility.getLogsUrl()}/archive?from=${from}`
  },
  getSearchLogsUrl: ( searchCriteria: string ) => {
    return `${UrlUtility.getLogsUrl()}/search?search=${searchCriteria}`
  },
  getTailLogsUrl: ( to: number ) => {
    return `${UrlUtility.getLogsUrl()}/tail?to=${to}`
  },
  getSettingsUrl: () => {
    return "/api/settings"
  },
  getSettingsLikesUrl: () => {
    return `${UrlUtility.getSettingsUrl()}/likes`
  },
  getSettingsRemoveTeaserUrl: ( teaser: string ) => {
    return `${UrlUtility.getSettingsUrl()}/teaser/${teaser}`
  },
  getSettingsUpdateApiKeyUrl: ( keyValue: string ) => {
    return `${UrlUtility.getSettingsUrl()}/token/${keyValue}`
  },
  getSettingsBaseUrl: ( urlValue: string ) => {
    return `${UrlUtility.getSettingsUrl()}/url/${urlValue}`
  },
  getSearchParameters: ( parameters: URLSearchParams, defaultPage: number, defaultSize: number ): Page => {
    const searchParameters: Page = { page: defaultPage, size: defaultSize }
    let page: number | string | null = parameters.get( "page" )
    let size: number | string | null = parameters.get( "size" )
    let search: string | null = parameters.get( "search" )
    let status: string | null = parameters.get( "status" )
    if ( page !== null ) {
      page = parseInt( page )
      searchParameters.page = Number.isNaN( page ) ? 1 : page
    }
    if ( size !== null ) {
      size = parseInt( size )
      searchParameters.size = Number.isNaN( size ) ? 10 : size
    }
    if ( search !== null && search.trim() !== "" ) {
      searchParameters.search = search
    }
    if ( status !== null && [ "liked", "scheduled", "new" ].indexOf( status ) !== -1 ) {
      searchParameters.status = status
    }
    return searchParameters
  }
}