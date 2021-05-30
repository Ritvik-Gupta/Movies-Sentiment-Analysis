import Axios from "axios"

export type AnalysisSuccess = {
	fetchState: string
	message: string
	movieReviews: string[]
	positiveReviewPercentage: number
}
export type AnalysisError = { error: string[] }
export type AnalysisResponse = AnalysisSuccess | AnalysisError

export const SentimentAnalysisApi = Axios.create({
	baseURL: process.env.NEXT_PUBLIC_SERVER_API_PATH!,
})
