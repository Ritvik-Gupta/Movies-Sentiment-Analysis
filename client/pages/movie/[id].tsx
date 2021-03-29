import { AxiosResponse } from "axios"
import { GetServerSideProps, NextPage } from "next"
import { ApiCompleteMovieResponse, ApiCompleteMovieResult, ImdbApi } from "services/api.imdb"

export interface IMovieProps {
	movie: ApiCompleteMovieResult
}

const Movie: NextPage<IMovieProps> = ({ movie }) => {
	console.log(movie)
	return null
}

export const getServerSideProps: GetServerSideProps<IMovieProps, { id: string }> = async ctx => {
	const { data }: AxiosResponse<ApiCompleteMovieResponse> = await ImdbApi({
		params: { plot: "full", i: ctx.params!.id },
	})
	if (typeof data === "string" || data.Response === "False") return { notFound: true }
	return { props: { movie: { ...data } } }
}
export default Movie
