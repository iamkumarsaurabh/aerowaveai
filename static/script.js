document.addEventListener("DOMContentLoaded", () => {

    setTimeout(() => {
        const dashboard = document.getElementById("weather-dashboard");
        const descElement = document.querySelector(".weather-desc") || document.querySelector(".condition-desc");
        const condition = descElement ? descElement.innerText.toLowerCase() : "clear";

        const bgElement = document.getElementById("weather-bg");
        const effectsContainer = document.getElementById("weather-effects");
        const weatherIcon = document.getElementById("weather-icon");

        let currentHour = new Date().getHours();
        if (dashboard && dashboard.hasAttribute("data-local-hour")) {
            const parsedHour = parseInt(dashboard.getAttribute("data-local-hour"));
            if (!isNaN(parsedHour)) {
                currentHour = parsedHour;
            }
        }

        let timeOfDay = "day";
        if (currentHour >= 18 && currentHour < 20) {
            timeOfDay = "evening";
        } else if (currentHour >= 20 || currentHour < 6) {
            timeOfDay = "night";
        }

        let bgClass = `bg-${timeOfDay}-clear`;

        // Premium AmCharts Animated SVGs (Guaranteed to work always)
        let iconSrc = "https://www.amcharts.com/wp-content/themes/amcharts4/css/img/icons/weather/animated/day.svg";

        if (condition.includes("cloud") || condition.includes("overcast") || condition.includes("mist") || condition.includes("haze")) {
            bgClass = timeOfDay === "night" ? "bg-night-clouds" : "bg-day-clouds";
            iconSrc = timeOfDay === "night" ?
                "https://www.amcharts.com/wp-content/themes/amcharts4/css/img/icons/weather/animated/cloudy-night-1.svg" :
                "https://www.amcharts.com/wp-content/themes/amcharts4/css/img/icons/weather/animated/cloudy-day-1.svg";
        } else if (condition.includes("rain") || condition.includes("drizzle")) {
            bgClass = "bg-rain";
            iconSrc = "https://www.amcharts.com/wp-content/themes/amcharts4/css/img/icons/weather/animated/rainy-1.svg";
        } else if (condition.includes("thunderstorm") || condition.includes("storm")) {
            bgClass = "bg-rain";
            iconSrc = "https://www.amcharts.com/wp-content/themes/amcharts4/css/img/icons/weather/animated/thunder.svg";
        } else if (timeOfDay === "night" && (condition.includes("clear") || condition.includes("sunny"))) {
            bgClass = "bg-night-clear";
            iconSrc = "https://www.amcharts.com/wp-content/themes/amcharts4/css/img/icons/weather/animated/night.svg";
        } else if (timeOfDay === "evening" && (condition.includes("clear") || condition.includes("sunny"))) {
            bgClass = "bg-evening-clear";
            iconSrc = "https://www.amcharts.com/wp-content/themes/amcharts4/css/img/icons/weather/animated/day.svg";
        }

        if (bgElement) bgElement.className = `dynamic-bg ${bgClass}`;

        if (weatherIcon) {
            weatherIcon.src = iconSrc;
        }

        if (effectsContainer) {
            effectsContainer.innerHTML = "";

            if (timeOfDay === "night") {
                for (let i = 0; i < 75; i++) {
                    let star = document.createElement("div");
                    star.className = "star";
                    star.style.width = Math.random() * 2.5 + "px";
                    star.style.height = star.style.width;
                    star.style.left = Math.random() * 100 + "vw";
                    star.style.top = Math.random() * 100 + "vh";
                    star.style.animationDuration = (Math.random() * 2 + 1) + "s";
                    effectsContainer.appendChild(star);
                }
            }

            if (condition.includes("rain") || condition.includes("drizzle") || condition.includes("thunderstorm")) {
                for (let i = 0; i < 95; i++) {
                    let drop = document.createElement("div");
                    drop.className = "raindrop";
                    drop.style.left = Math.random() * 100 + "vw";
                    drop.style.animationDuration = (Math.random() * 0.4 + 0.4) + "s";
                    drop.style.animationDelay = Math.random() * 2 + "s";
                    effectsContainer.appendChild(drop);
                }
            }

            if (condition.includes("cloud") || condition.includes("overcast") || condition.includes("mist") || condition.includes("haze")) {
                for (let i = 0; i < 5; i++) {
                    let cloud = document.createElement("div");
                    cloud.className = "bg-cloud";
                    cloud.style.width = (Math.random() * 220 + 160) + "px";
                    cloud.style.height = (Math.random() * 75 + 45) + "px";
                    cloud.style.top = (Math.random() * 38) + "vh";
                    cloud.style.animationDuration = (Math.random() * 28 + 38) + "s";
                    cloud.style.animationDelay = "-" + (Math.random() * 18) + "s";
                    effectsContainer.appendChild(cloud);
                }
            }
        }
    }, 100);
});