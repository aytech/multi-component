import { Pagination } from "antd"
import { UsersData } from "../../lib/types"

interface Props {
  userData: UsersData | null
}

export const Paginator = ( { userData }: Props ) => {
  return userData !== null ? (
    <Pagination
      className="pagination"
      showSizeChanger
      onShowSizeChange={ ( current: any, pageSize: any ) => { console.log( current, pageSize ) } }
      defaultCurrent={ 1 }
      total={ userData.total }
    />
  ) : null
}