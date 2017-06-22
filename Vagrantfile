# frozen_string_literal: true

VAGRANTFILE_API_VERSION = "2"
ENV['VAGRANT_DEFAULT_PROVIDER'] ||= "virtualbox"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/xenial64"
  
  config.vm.provider :virtualbox do |vb|
    vb.gui    = false
    vb.name   = "apex_sigma_bot"
    vb.memory = 1024
    vb.cpus   = 2
  end
  
  config.vm.provision "bootstrap", type: :shell do |s|
    s.path = "bin/vagrant/bootstrap.sh"
  end

  config.vm.provision "bot", type: :shell, run: :always do |s|
    s.path = "bin/vagrant/start.sh"
  end
end
