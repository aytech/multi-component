import { Page } from "./types"

export const UrlUtility = {
  getUserSearchUrl: ( page: Page ) => {
    let url = `/api/users/search/${ page.search }?page=${ page.page }&size=${ page.size }`
    if ( page.liked !== undefined ) {
      url += `&liked=${ page.liked }`
    }
    return url
  },
  getUsersUrl: ( page: Page ) => {
    let url = `/api/users?page=${ page.page }&size=${ page.size }`
    if ( page.liked !== undefined ) {
      url += `&liked=${ page.liked }`
    }
    return url
  },
  getLogsUrl: ( chunk_size: number, from: number | null ) => {
    let url: string = `/api/logs?limit=${ chunk_size }`
    if ( from !== null ) {
      url += `&from=${ from }`
    }
    return url
  },
  getTeaserListsUrl: () => {
    return "/api/settings/teasers"
  },
  getSettingsLikesUrl: () => {
    return "/api/settings/likes"
  },
  getSearchParameters: ( parameters: URLSearchParams, defaultPage: number, defaultSize: number ): Page => {
    const searchParameters: Page = { page: defaultPage, size: defaultSize }
    let page: number | string | null = parameters.get( "page" )
    let size: number | string | null = parameters.get( "size" )
    let search: string | null = parameters.get( "search" )
    let liked: string | null = parameters.get( "liked" )
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
    if ( liked !== null && [ "0", "1" ].indexOf( liked ) !== -1 ) {
      searchParameters.liked = liked
    }
    return searchParameters
  }
}