export interface Profile {
  city?: string
  id: number
  liked: boolean
  name: string
  photos: Array<Photo>
  s_number: number
  user_id: string
}

export interface Photo {
  photo_id: string
  url: string
}

export interface UsersData {
  total: number,
  users: Array<Profile>
}

export interface Page {
  liked?: string
  page: number
  search?: string
  size: number
}

export interface Log {
  created: string,
  id: number,
  text: string
}

export interface LogsData {
  last: boolean
  logs: Array<Log>
}

export interface TeaserData {
  teasers: Array<string>
}