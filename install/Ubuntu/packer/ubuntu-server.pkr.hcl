variable "build_directory" {
    default = "./build"
}

variable "boot_wait" {
    default = "6s"
}

variable "cpus" {
    default = 2
}

variable "disk_size" {
    default = 60000
}

variable "headless" {
    default = false
}

variable "http_directory" {
    default = "./subiquity/http"
}

variable "iso_url" {
    type = string
}

variable "iso_checksum" {
    type = string
}

variable "memory" {
    default = 8192
}

variable "template" {
    type = string
}

variable "username" {
    default = "cyber"
}

variable "password" {
    default = "ITIS6010"
}

variable "vm_name" {
    type = string
}

variable "provider_name" {
    default = "virtualbox"
}

variable "ssh_timeout" {
    default = "45m"
}

variable "gfx_controller" {
    default = "vmsvga"
}

variable "gfx_vram_size" {
    default = 16
}


source "virtualbox-iso" "ubuntu_server" {

    boot_command = [
        "c<wait>",
        "set gfxpayload=keep<enter>",
        "linux /casper/vmlinuz --- autoinstall quiet 'ds=nocloud-net;s=http://{{ .HTTPIP }}:{{ .HTTPPort }}/'",
        "<enter>",
        "initrd /casper/initrd<enter>",
        "boot<enter>"
    ]

    boot_wait            = var.boot_wait
    cpus                 = var.cpus
    disk_size            = var.disk_size
    guest_os_type        = "Ubuntu_64"
    hard_drive_interface = "sata"
    headless             = var.headless
    http_directory       = var.http_directory
    iso_url              = var.iso_url
    iso_checksum         = var.iso_checksum
    memory               = var.memory
    output_directory     = "${var.build_directory}/packer-${var.template}-${var.provider_name}"
    shutdown_command     = "echo '${var.username}' | sudo -S shutdown -P now"
    ssh_timeout          = var.ssh_timeout
    ssh_username         = var.username
    ssh_password         = var.password
    gfx_controller       = var.gfx_controller
    gfx_vram_size        = var.gfx_vram_size
    vm_name              = var.vm_name
}

build {
    sources = ["sources.virtualbox-iso.ubuntu_server"]
    provisioner "shell" {
        script = "packages.sh"
    }
    provisioner "shell" {
        script = "virtualbox-guest-additions.sh"
        remote_path = "/home/cyber/virtualbox-guest-additions.sh"
    }
    provisioner "file" {
        source = "camflow debs/"
        destination = "/tmp"
    }
    provisioner "shell" {
        script = "flurry-ubuntu-packer.sh"
        remote_path = "/home/cyber/flurry-ubuntu.sh"
    }
}
