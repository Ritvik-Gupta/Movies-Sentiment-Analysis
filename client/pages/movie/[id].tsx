import Container from "@material-ui/core/Container"
import { createStyles, makeStyles } from "@material-ui/core/styles"
import { AxiosResponse } from "axios"
import { GetServerSideProps, NextPage } from "next"
import { ApiCompleteMovieResponse, ApiCompleteMovieResult, ImdbApi } from "services/api.imdb"

const useStyles = makeStyles(() =>
	createStyles({
		container: {
			paddingTop: 15,
		},
	})
)

export interface IMovieProps {
	movie: ApiCompleteMovieResult
}

const Movie: NextPage<IMovieProps> = ({ movie }) => {
	const classes = useStyles()

	console.log(movie)
	return (
		<Container className={classes.container} fixed>
			<div>something</div>
		</Container>
	)
}

export const getServerSideProps: GetServerSideProps<IMovieProps, { id: string }> = async ctx => {
	const { data }: AxiosResponse<ApiCompleteMovieResponse> = await ImdbApi({
		params: { plot: "full", i: ctx.params!.id },
	})
	if (typeof data === "string" || data.Response === "False") return { notFound: true }
	return { props: { movie: data } }
}
export default Movie
