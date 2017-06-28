#第三方库生成framework使用，用于将素有pods里的scheme设为shared状态

require 'cocoapods'
require 'cocoapods-core'

def sharePodSchemes(pods_project_path)
    project = Xcodeproj::Project.open(pods_project_path)
	project.targets.each { |e| 
  	if e.product_type == 'com.apple.product-type.framework' && !e.name.start_with?('Pod')
    	begin  
      		Xcodeproj::XCScheme.share_scheme(project.path, e.name)
      		puts "Success share #{e.name}" 
    	rescue => err  
      		puts "Fail share #{e.name}"   
    	end 
  	end
	}
	project.save
end

sharePodSchemes(ARGV.first)