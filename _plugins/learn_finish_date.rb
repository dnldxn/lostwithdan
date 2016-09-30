require 'time'
require 'json'

module Reading
  class Generator < Jekyll::Generator
    def generate(site)
        data_dir = site.config['data_dir']
        # Jekyll.logger.info site.data

        pois = site.data['atdb092116023143ALL']
        # Jekyll.logger.info coords

        dist_per_day = {}
        dist_completed = 0
        dist_remaining = 0

        pois.each_with_index do |poi, index|
            if index > 0
                # lat1 = pois[index-1]['lat'].to_f
                # lng1 = pois[index-1]['lon'].to_f
                # lat2 = poi['lat'].to_f
                # lng2 = poi['lon'].to_f

                prev_mileage = pois[index-1]['to_spgr'].to_f
                mileage = pois[index]['to_spgr'].to_f
                if ( pois[index]['dt_reached'] )
                    prev_dt_tm = Time.parse( pois[index-1]['dt_reached'] )
                    dt_tm = Time.parse( poi['dt_reached'] )
                    # dt.class.name

                    dt_str = dt_tm.to_date.to_s
                    dist_per_day[dt_str] = dist_per_day.fetch(dt_str, 0.0) + ( mileage - prev_mileage )
                    dist_completed = poi['to_spgr']
                    dist_remaining = poi['to_ktd']

                    #pace =  (mileage - prev_mileage) / ( (dt - prev_dt) / 3600 )
                    #date_diff = dt - prev_dt
                    #Jekyll.logger.info "Mileage #{prev_mileage}, #{mileage}, Date #{prev_dt}, #{dt} (#{date_diff}) is #{pace}"
                end
            end
        end

        # Jekyll.logger.info dist_per_day
        File.open(data_dir + "/stats.csv", "w+") do |f|
            # f.puts("dist_completed: " + dist_completed)
            # f.puts("dist_remaining: " + dist_remaining)
            # f.puts("dist_per_day: " + dist_per_day.to_json)
        end
    end

    # def distance(lat1, lon1, lat2, lon2)
    #     p = 0.017453292519943295    # Math.PI / 180
    #     a = 0.5 - Math.cos((lat2 - lat1) * p) / 2 + Math.cos(lat1 * p) * Math.cos(lat2 * p) * (1 - Math.cos((lon2 - lon1) * p)) / 2

    #     return 12742 * 0.621371 * Math.asin(Math.sqrt(a))  # 2 * R; R = 6371 km; 0.62 km to miles
    # end

  end
end