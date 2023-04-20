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
  page: number
  search?: string
  size: number
}