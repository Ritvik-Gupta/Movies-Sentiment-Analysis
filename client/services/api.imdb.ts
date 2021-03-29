import Axios from "axios"

type ApiSuccess<T extends Record<string, any>> = { Response: "True" } & T
type ApiError = { Response: "False"; Error: string }
type ApiResponse<T extends Record<string, any>> = ApiSuccess<T> | ApiError

type MovieType = "movie" | "series" | "episode"
export type ApiSearchResult = {
	Type: MovieType
} & Record<"imdbID" | "Title" | "Year" | "Poster", string>

export type ApiSearchResponse = ApiResponse<{
	Search: ApiSearchResult[]
	totalResults: string
}>

export type ApiCompleteMovieResult = {
	Ratings: { Source: string; Value: string }[]
} & ApiSearchResult &
	Record<
		| "Rated"
		| "Released"
		| "Runtime"
		| "Genre"
		| "Director"
		| "Writer"
		| "Actors"
		| "Plot"
		| "Language"
		| "Country"
		| "Awards"
		| "Metascore"
		| "imdbRating"
		| "imdbVotes"
		| "DVD"
		| "BoxOffice"
		| "Production"
		| "Website",
		string
	>

export type ApiCompleteMovieResponse = ApiResponse<ApiCompleteMovieResult> | string

export const ImdbApi = Axios.create({
	baseURL: process.env.NEXT_PUBLIC_OMDB_API_PATH!,
	params: { apiKey: process.env.NEXT_PUBLIC_OMDB_API_KEY! },
})
