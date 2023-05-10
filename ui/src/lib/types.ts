export interface Profile {
  age: number
  bio: string
  birth_date: string
  city: string
  created: string
  distance: number
  id: number
  liked: boolean
  name: string
  photos: Array<Photo>
  s_number: number
  scheduled: boolean
  user_id: string
}

export interface Photo {
  photo_id: string
  url: string
}

export interface UsersData {
  total: number
  users: Array<Profile>
}

export interface Page {
  page: number
  search?: string
  size: number
  status?: string
}

export interface Log {
  created: string
  id: number
  text: string
}

export interface LogsData {
  logs: Array<Log>
}

export interface SettingsData {
  api_key: string
  base_url: string
  scheduled: number
  teasers: Array<string>
}

export interface LikesData {
  likes_remaining: number
  rate_limited_until: string
}

export interface SettingsOtherData {
  additionalDescription?: string
  additionalValue?: number | string
  description: string
  key: number
  value: number
}