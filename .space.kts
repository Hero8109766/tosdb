job("Build and push Docker") {
    docker {
        build {
            context = "docker"
            file = "./Dockerfile"
            labels["vendor"] = "ebisuke"
        }

        push("ebisuke/p/tos/tos/tos-database") {
            // use current job run number as a tag - '0.0.run_number'
            tags("0.0.\$JB_SPACE_EXECUTION_NUMBER")
            // see example on how to use branch name in a tag
        }
    }
}