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
  photoId: string
  url: string
}

export interface UsersData {
  total: number
  profiles: Array<Profile>
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

export interface TeaserData {
  loading: boolean
  name: string
}

export interface SettingsRawData {
  apiKey: string
  baseUrl: string
  scheduled: number
  teasers: Array<string>
}

export interface SettingsData {
  apiKey: string
  baseUrl: string
  scheduled: number
  teasers: Array<TeaserData>
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

export interface SettingsRemoveTeaserResponse {
  success: boolean
  message: string
}